class FindingStore:


    def __init__(self):

        self.findings = []


    def save(self, finding):

        self.findings.append(
            finding
        )


    def all(self):

        return self.findings
