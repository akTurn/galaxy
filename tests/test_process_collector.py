from collectors.process import ProcessCollector


collector = ProcessCollector()

observations = collector.collect()

for observation in observations[:5]:
    print(observation)
