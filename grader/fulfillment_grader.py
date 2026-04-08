class FulfillmentGrader:
    def grade(self, env):
        completed = len(env.completed_orders)
        delayed = len(env.delayed_orders)
        total = completed + delayed

        if total == 0:
            return 0.0

        score = completed / total
        score -= 0.2 * (delayed / total)

        return max(0.0, min(1.0, score))