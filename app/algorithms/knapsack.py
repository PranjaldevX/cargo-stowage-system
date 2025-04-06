def optimize_waste(items, max_weight):
        """
            0/1 Knapsack implementation for waste optimization.
                Args:
                        items: List of dicts with {'itemId', 'mass', 'priority'}
                                max_weight: Maximum allowed weight (kg)
                                    Returns:
                                            Dict with selected items, total weight, and priority score
                                                """
                                                    n = len(items)
                                                        # DP table: rows = items, cols = weights
                                                            dp = [[0] * (max_weight + 1) for _ in range(n + 1)]
                                                                
                                                                    # Build DP table
                                                                        for i in range(1, n + 1):
                                                                                item = items[i-1]
                                                                                        for w in range(1, max_weight + 1):
                                                                                                    if item["mass"] <= w:
                                                                                                                    dp[i][w] = max(
                                                                                                                                        dp[i-1][w],
                                                                                                                                                            dp[i-1][w - int(item["mass"])] + item["priority"]
                                                                                                                                                                            )
                                                                                                                                                                                        else:
                                                                                                                                                                                                        dp[i][w] = dp[i-1][w]
                                                                                                                                                                                                            
                                                                                                                                                                                                                # Backtrack to find selected items
                                                                                                                                                                                                                    selected_items = []
                                                                                                                                                                                                                        w = max_weight
                                                                                                                                                                                                                            for i in range(n, 0, -1):
                                                                                                                                                                                                                                    if dp[i][w] != dp[i-1][w]:
                                                                                                                                                                                                                                                selected_items.append(items[i-1]["itemId"])
                                                                                                                                                                                                                                                            w -= int(items[i-1]["mass"])
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                    return {
                                                                                                                                                                                                                                                                            "selected_items": selected_items,
                                                                                                                                                                                                                                                                                    "total_weight": sum(item["mass"] for item in items if item["itemId"] in selected_items),
                                                                                                                                                                                                                                                                                            "total_priority": dp[n][max_weight]
                                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                                # Test case
                                                                                                                                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                    test_items = [
                                                                                                                                                                                                                                                                                                            {"itemId": "waste1", "mass": 5, "priority": 30},
                                                                                                                                                                                                                                                                                                                    {"itemId": "waste2", "mass": 3, "priority": 50},
                                                                                                                                                                                                                                                                                                                            {"itemId": "waste3", "mass": 4, "priority": 40}
                                                                                                                                                                                                                                                                                                                                ]
                                                                                                                                                                                                                                                                                                                                    print(optimize_waste(test_items, 7))