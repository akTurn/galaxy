class ProcessIdentity:
    #added type hints and a return type.
    @staticmethod
    def from_process(pid: int, create_time: float) -> str:
        return f"pid:{pid}@{create_time}"


#  could simply write:

# f"pid:{pid}@{create_time}"

# everywhere.

# But that would spread identity logic throughout Galaxy.

# Instead:

# ProcessIdentity
#        │
#        ▼
# one place defines identity

# Later, if  change the identity format,  change one place.

# That's good architecture.

# class ProcessIdentity:

#     @staticmethod
#     def from_process(pid, create_time):
#         return f"pid:{pid}@{create_time}"
