# class FindingStore:

#     def __init__(self):
#         self.findings = {}

#     def add(self, finding):
#         self.findings[finding.id] = finding

class FindingStore:

    def __init__(self):
        self.findings = {}

    def add(self, finding):

        existing = self.findings.get(
            finding.id
        )

        if existing is None:

            self.findings[finding.id] = finding

            return finding

        existing.last_seen = finding.last_seen

        existing.occurrences += 1

        existing.status = "active"

        existing.evidence = finding.evidence

        return existing