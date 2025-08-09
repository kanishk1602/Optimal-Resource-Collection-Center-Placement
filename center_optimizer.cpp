#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <unordered_map>
#include <set>
#include <algorithm>
#include <cmath>
#include <limits>
#include <random>
#include <chrono>

struct Point
{
    int id;
    double lat, lon;
    double resource_quantity;
    std::string land_type;
    double slope;
    double elevation;

    Point() : id(0), lat(0), lon(0), resource_quantity(0), slope(0), elevation(0) {}
};

class KMedoidsOptimizer
{
private:
    std::vector<Point> points;
    std::unordered_map<std::string, std::unordered_map<std::string, double>> distance_matrix;
    std::vector<int> valid_candidates;
    int k;
    double min_distance_km;
    std::set<std::string> exclude_land_types;
    double max_slope;

    std::mt19937 rng;

public:
    KMedoidsOptimizer(int k_val, double min_dist, const std::set<std::string> &exclude_types, double max_slope_val)
        : k(k_val), min_distance_km(min_dist), exclude_land_types(exclude_types), max_slope(max_slope_val)
    {
        rng.seed(std::chrono::steady_clock::now().time_since_epoch().count());
    }

    void load_points(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Error: Cannot open " << filename << std::endl;
            return;
        }

        std::string line;
        std::getline(file, line); // Skip header

        while (std::getline(file, line))
        {
            std::istringstream ss(line);
            std::string token;
            Point p;

            // Parse CSV: id,latitude,longitude,resource_quantity
            if (std::getline(ss, token, ','))
                p.id = std::stoi(token);
            if (std::getline(ss, token, ','))
                p.lat = std::stod(token);
            if (std::getline(ss, token, ','))
                p.lon = std::stod(token);
            if (std::getline(ss, token, ','))
                p.resource_quantity = std::stod(token);

            points.push_back(p);
        }
        file.close();
        std::cout << "Loaded " << points.size() << " resource points" << std::endl;
    }

    void load_zone_features(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Error: Cannot open " << filename << std::endl;
            return;
        }

        std::string line;
        std::getline(file, line); // Skip header

        std::map<int, Point> zone_map;
        while (std::getline(file, line))
        {
            std::istringstream ss(line);
            std::string token;
            Point zone;

            // Parse CSV: id,slope,elevation,land_type
            if (std::getline(ss, token, ','))
                zone.id = std::stoi(token);
            if (std::getline(ss, token, ','))
                zone.slope = std::stod(token);
            if (std::getline(ss, token, ','))
                zone.elevation = std::stod(token);
            if (std::getline(ss, token, ','))
                zone.land_type = token;

            zone_map[zone.id] = zone;
        }
        file.close();

        // Merge zone features with points
        for (auto &point : points)
        {
            if (zone_map.find(point.id) != zone_map.end())
            {
                const Point &zone = zone_map[point.id];
                point.land_type = zone.land_type;
                point.slope = zone.slope;
                point.elevation = zone.elevation;
            }
        }
        std::cout << "Loaded zone features for " << zone_map.size() << " locations" << std::endl;
    }

    void load_distances(const std::string &filename)
    {
        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Error: Cannot open " << filename << std::endl;
            return;
        }

        std::string line;
        std::getline(file, line); // Header with point IDs

        int row = 0;
        while (std::getline(file, line))
        {
            std::istringstream ss(line);
            std::string token;
            std::getline(ss, token, ','); // Skip row label

            int col = 0;
            while (std::getline(ss, token, ','))
            {
                if (row < points.size() && col < points.size())
                {
                    double dist = std::stod(token);
                    std::string from_key = std::to_string(points[row].id);
                    std::string to_key = std::to_string(points[col].id);
                    distance_matrix[from_key][to_key] = dist * 1000; // Convert km to meters
                }
                col++;
            }
            row++;
        }
        file.close();
        std::cout << "Loaded distance matrix" << std::endl;
    }

    double get_distance(int from_id, int to_id)
    {
        std::string from_key = std::to_string(from_id);
        std::string to_key = std::to_string(to_id);

        if (distance_matrix.find(from_key) != distance_matrix.end() &&
            distance_matrix[from_key].find(to_key) != distance_matrix[from_key].end())
        {
            return distance_matrix[from_key][to_key];
        }

        // Fallback to Haversine distance
        Point from_point, to_point;
        for (const auto &p : points)
        {
            if (p.id == from_id)
                from_point = p;
            if (p.id == to_id)
                to_point = p;
        }

        return haversine_distance(from_point.lat, from_point.lon, to_point.lat, to_point.lon);
    }

    double haversine_distance(double lat1, double lon1, double lat2, double lon2)
    {
        const double R = 6371000; // Earth radius in meters
        double dlat = (lat2 - lat1) * M_PI / 180.0;
        double dlon = (lon2 - lon1) * M_PI / 180.0;
        double a = sin(dlat / 2) * sin(dlat / 2) + cos(lat1 * M_PI / 180.0) * cos(lat2 * M_PI / 180.0) * sin(dlon / 2) * sin(dlon / 2);
        double c = 2 * atan2(sqrt(a), sqrt(1 - a));
        return R * c;
    }

    void filter_candidates()
    {
        valid_candidates.clear();

        for (int i = 0; i < points.size(); i++)
        {
            const Point &p = points[i];

            // Check land type exclusions
            if (exclude_land_types.find(p.land_type) != exclude_land_types.end())
            {
                continue;
            }

            // Check slope constraint
            if (p.slope > max_slope)
            {
                continue;
            }

            valid_candidates.push_back(i);
        }

        std::cout << "Valid candidates after filtering: " << valid_candidates.size() << std::endl;
    }

    bool satisfies_min_distance(const std::vector<int> &medoids, int new_candidate)
    {
        for (int medoid_idx : medoids)
        {
            double dist = get_distance(points[new_candidate].id, points[medoid_idx].id);
            if (dist < min_distance_km * 1000)
            { // Convert km to meters
                return false;
            }
        }
        return true;
    }

    double calculate_total_cost(const std::vector<int> &medoids)
    {
        double total_cost = 0.0;

        for (int i = 0; i < points.size(); i++)
        {
            double min_dist = std::numeric_limits<double>::max();

            for (int medoid_idx : medoids)
            {
                double dist = get_distance(points[i].id, points[medoid_idx].id);
                min_dist = std::min(min_dist, dist);
            }

            total_cost += min_dist * points[i].resource_quantity;
        }

        return total_cost;
    }

    std::vector<int> get_assignments(const std::vector<int> &medoids)
    {
        std::vector<int> assignments(points.size());

        for (int i = 0; i < points.size(); i++)
        {
            double min_dist = std::numeric_limits<double>::max();
            int best_medoid = -1;

            for (int j = 0; j < medoids.size(); j++)
            {
                double dist = get_distance(points[i].id, points[medoids[j]].id);
                if (dist < min_dist)
                {
                    min_dist = dist;
                    best_medoid = j;
                }
            }

            assignments[i] = best_medoid;
        }

        return assignments;
    }

    std::vector<int> initialize_medoids()
    {
        std::vector<int> medoids;
        std::vector<int> available_candidates = valid_candidates;

        // First medoid: random selection
        if (!available_candidates.empty())
        {
            std::uniform_int_distribution<int> dist(0, available_candidates.size() - 1);
            int first_idx = dist(rng);
            medoids.push_back(available_candidates[first_idx]);
        }

        // Subsequent medoids: ensure minimum distance constraint
        for (int i = 1; i < k && !available_candidates.empty(); i++)
        {
            std::vector<int> valid_next;

            for (int candidate_idx : available_candidates)
            {
                if (std::find(medoids.begin(), medoids.end(), candidate_idx) == medoids.end() &&
                    satisfies_min_distance(medoids, candidate_idx))
                {
                    valid_next.push_back(candidate_idx);
                }
            }

            if (valid_next.empty())
            {
                std::cout << "Warning: Cannot find " << k << " medoids satisfying distance constraint" << std::endl;
                break;
            }

            std::uniform_int_distribution<int> dist(0, valid_next.size() - 1);
            medoids.push_back(valid_next[dist(rng)]);
        }

        return medoids;
    }

    std::pair<std::vector<int>, double> optimize()
    {
        filter_candidates();

        if (valid_candidates.size() < k)
        {
            std::cout << "Error: Not enough valid candidates (" << valid_candidates.size() << ") for k=" << k << std::endl;
            return {{}, std::numeric_limits<double>::max()};
        }

        std::vector<int> best_medoids = initialize_medoids();
        double best_cost = calculate_total_cost(best_medoids);

        std::cout << "Initial cost: " << best_cost << std::endl;

        bool improved = true;
        int iterations = 0;
        const int max_iterations = 50;

        while (improved && iterations < max_iterations)
        {
            improved = false;
            iterations++;

            for (int i = 0; i < best_medoids.size(); i++)
            {
                for (int candidate_idx : valid_candidates)
                {
                    if (std::find(best_medoids.begin(), best_medoids.end(), candidate_idx) != best_medoids.end())
                    {
                        continue; // Already a medoid
                    }

                    // Create new medoid set with replacement
                    std::vector<int> new_medoids = best_medoids;
                    new_medoids[i] = candidate_idx;

                    // Check minimum distance constraint
                    bool valid = true;
                    for (int j = 0; j < new_medoids.size(); j++)
                    {
                        for (int l = j + 1; l < new_medoids.size(); l++)
                        {
                            double dist = get_distance(points[new_medoids[j]].id, points[new_medoids[l]].id);
                            if (dist < min_distance_km * 1000)
                            {
                                valid = false;
                                break;
                            }
                        }
                        if (!valid)
                            break;
                    }

                    if (!valid)
                        continue;

                    double new_cost = calculate_total_cost(new_medoids);
                    if (new_cost < best_cost)
                    {
                        best_medoids = new_medoids;
                        best_cost = new_cost;
                        improved = true;
                    }
                }
            }

            if (improved)
            {
                std::cout << "Iteration " << iterations << ": cost = " << best_cost << std::endl;
            }
        }

        std::cout << "Converged after " << iterations << " iterations" << std::endl;
        return {best_medoids, best_cost};
    }

    void print_results(const std::vector<int> &medoids, double total_cost)
    {
        std::cout << "\nBest Centers:" << std::endl;
        for (int medoid_idx : medoids)
        {
            const Point &p = points[medoid_idx];
            std::cout << p.id << "," << p.lat << "," << p.lon << ","
                      << p.land_type << "," << p.slope << "," << p.elevation << std::endl;
        }

        std::cout << "\nAssignments:" << std::endl;
        std::vector<int> assignments = get_assignments(medoids);
        for (int i = 0; i < points.size(); i++)
        {
            std::cout << "Point: " << points[i].id << " -> Center: "
                      << points[medoids[assignments[i]]].id << std::endl;
        }

        std::cout << "\nTotal Cost: " << total_cost << std::endl;
    }
};

int main(int argc, char *argv[])
{
    if (argc < 5)
    {
        std::cerr << "Usage: " << argv[0] << " <resource_points.csv> <zone_features.csv> <road_network.csv> <k> [min_distance_km] [exclude_land_types] [max_slope]" << std::endl;
        return 1;
    }

    std::string resource_file = argv[1];
    std::string zone_file = argv[2];
    std::string road_file = argv[3];
    int k = std::stoi(argv[4]);

    double min_distance_km = (argc > 5) ? std::stod(argv[5]) : 2.0;
    std::set<std::string> exclude_types;
    if (argc > 6 && std::string(argv[6]) != "none")
    {
        std::string exclude_str = argv[6];
        std::istringstream ss(exclude_str);
        std::string token;
        while (std::getline(ss, token, ','))
        {
            exclude_types.insert(token);
        }
    }
    double max_slope = (argc > 7) ? std::stod(argv[7]) : 30.0;

    KMedoidsOptimizer optimizer(k, min_distance_km, exclude_types, max_slope);

    optimizer.load_points(resource_file);
    optimizer.load_zone_features(zone_file);
    optimizer.load_distances(road_file);

    auto [medoids, cost] = optimizer.optimize();

    if (!medoids.empty())
    {
        optimizer.print_results(medoids, cost);
    }
    else
    {
        std::cout << "No valid solution found" << std::endl;
        return 1;
    }

    return 0;
}