from collectors.network import NetworkCollector


collector = NetworkCollector()

observations = collector.collect()

print(f"Network interfaces found: {len(observations)}")

for observation in observations:

    print()
    print("Entity:", observation.entity_id)
    print("Data:", observation.data)
