class FulfillmentGrader:
    def grade(self, env):
        completed = len(env.completed_orders)
        delayed = len(env.delayed_orders)
        total = completed + delayed

        if total == 0:
            return 0.01  # avoid 0

        score = completed / total

        # penalty for delays
        score -= 0.2 * (delayed / total)

        # 🔥 CRITICAL FIX: clamp strictly between (0,1)
        if score <= 0:
            score = 0.01
        elif score >= 1:
            score = 0.99

        return score
