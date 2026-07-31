from difflib import SequenceMatcher


class Deduplicator:
    SIMILARITY_THRESHOLD = 0.82

    def deduplicate(self, candidates):
        if not candidates:
            return []
        groups = self._group_similar(candidates)
        merged = []
        for group in groups:
            if len(group) == 1:
                merged.append(group[0])
            else:
                merged.append(self._merge_group(group))
        return merged

    def _group_similar(self, candidates):
        grouped = []
        assigned = set()
        for i, c1 in enumerate(candidates):
            if i in assigned:
                continue
            group = [c1]
            assigned.add(i)
            c1_concept = c1.get("concept", "").lower().strip()
            for j, c2 in enumerate(candidates):
                if j in assigned:
                    continue
                c2_concept = c2.get("concept", "").lower().strip()
                similarity = SequenceMatcher(None, c1_concept, c2_concept).ratio()
                if similarity >= self.SIMILARITY_THRESHOLD:
                    group.append(c2)
                    assigned.add(j)
            grouped.append(group)
        return grouped

    def _merge_group(self, group):
        best = max(group, key=lambda x: x.get("confidence", 0))
        merged = dict(best)
        all_definitions = [c.get("definition", "") for c in group if c.get("definition", "")]
        all_scenarios = [c.get("real_world_scenario", "") for c in group if c.get("real_world_scenario", "")]
        all_clozes = [c.get("case_study_cloze", "") for c in group if c.get("case_study_cloze", "")]
        all_related = set()
        for c in group:
            for rc in c.get("related_concepts", []):
                all_related.add(rc)
        all_strategies = list(set(c.get("strategy", "") for c in group))
        if not merged.get("definition") and all_definitions:
            merged["definition"] = max(all_definitions, key=len)
        if not merged.get("real_world_scenario") and all_scenarios:
            merged["real_world_scenario"] = max(all_scenarios, key=len)
        if not merged.get("case_study_cloze") and all_clozes:
            merged["case_study_cloze"] = max(all_clozes, key=len)
        if all_related:
            merged["related_concepts"] = sorted(all_related)[:5]
        merged["merged_strategies"] = all_strategies
        merged["merged_count"] = len(group)
        avg_confidence = sum(c.get("confidence", 0) for c in group) / len(group)
        merged["confidence"] = min(0.98, avg_confidence + 0.05 * (len(group) - 1) / max(len(group), 1))
        return merged
