from collectors.service import ServiceCollector


collector = ServiceCollector()

observations = collector.collect()

print("Services found:", len(observations))

for observation in observations[:20]:

    print()
    print("Entity:", observation.entity_id)
    print("Data:", observation.data)

print()
print("--- services with a live main_pid ---")

for observation in observations:

    if observation.data.get("main_pid"):
        print(observation.entity_id, "-> pid", observation.data["main_pid"])



# from collectors.service import ServiceCollector


# collector = ServiceCollector()

# observations = collector.collect()

# print("Services found:", len(observations))

# for observation in observations[:20]:

#     print()
#     print("Entity:", observation.entity_id)
#     print("Data:", observation.data)


