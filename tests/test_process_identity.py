from core.models.process_identity import ProcessIdentity


identity = ProcessIdentity.from_process(
    39038,
    1788949759.16
)

print(identity)


first = ProcessIdentity.from_process(
        39038,
        1788949759.18
    )

second = ProcessIdentity.from_process(
        39038,
        1788955000.42
    )

print(first)
print(second)

assert first != second


first = ProcessIdentity.from_process(
    39038,
    1788949759.18
)

same_process = ProcessIdentity.from_process(
    39038,
    1788949759.18
)


print(first)
print(same_process)

assert first == same_process

# # And the important assertion:

# # assert first != second

# # proves:

# # same PID
# # +
# # different creation time
# # =
# # different process identity

# Exactly — this is an important distinction.

#  If you **print two different values**, you can visually see that they're different:

# ```
# first = ProcessIdentity.from_process(39038, 1788949759.18)
# second = ProcessIdentity.from_process(39038, 1788955000.42)

# print(first)
# print(second)
# ```

#  You get:

# ```
# pid:39038@1788949759.18
# pid:39038@1788955000.42
# ```

#  So **for learning/debugging**, that's enough.

#  But `assert` has a different purpose: it turns your expectation into an **automatic test**.

#  ## Without `assert`

# ```
# print(first)
# print(second)
# ```

#  You're basically saying:

#  > "Look at these and decide whether they're correct."

#  A human has to inspect the output.

# ---

#  ## With `assert`

# ```
# assert first != second
# ```

#  You're saying:

#  > "Python, verify that these two identities are different. If they aren't, tell me the test failed."

#  If correct:

# ```
# Process finishes successfully
# ```

#  If something breaks and both identities become equal:

# ```
# AssertionError
# ```

#  That's much more useful as the project grows.

# ---

#  ## Imagine we accidentally break the implementation

#  Suppose somebody changes:

# ```
# class ProcessIdentity:

#     @staticmethod
#     def from_process(pid, create_time):
#         return f"pid:{pid}"
# ```

#  Now:

# ```
# first = ProcessIdentity.from_process(39038, 1788949759.18)
# second = ProcessIdentity.from_process(39038, 1788955000.42)
# ```

#  Both become:

# ```
# pid:39038
# pid:39038
# ```

#  If we only have:

# ```
# print(first)
# print(second)
# ```

#  the program still runs.

#  You have to notice:

# ```
# "Oh... those shouldn't be equal."
# ```

#  But with:

# ```
# assert first != second
# ```

#  Python immediately tells you:

# ```
# AssertionError
# ```

#  So the test catches the regression automatically.

# ---

#  # There's an even better test here

#  Because our requirement is specifically:

#  > Same PID + different creation time must produce different identities.

#  We can express exactly that:

# ```
# from core.models.process_identity import ProcessIdentity

# def main():

#     first = ProcessIdentity.from_process(
#         39038,
#         1788949759.18
#     )

#     second = ProcessIdentity.from_process(
#         39038,
#         1788955000.42
#     )

#     assert first != second

#     print("Process identity test passed")

# if __name__ == "__main__":
#     main()
# ```

#  Now the output is:

# ```
# Process identity test passed
# ```

#  The important thing is that the message only appears **after the assertion succeeds**.

# ---

#  ## And we can test the other side too

#  We don't only want:

# ```
# different creation time → different identity
# ```

#  We also want:

# ```
# same PID + same creation time → same identity
# ```

#  So:

# ```
# first = ProcessIdentity.from_process(
#     39038,
#     1788949759.18
# )

# same_process = ProcessIdentity.from_process(
#     39038,
#     1788949759.18
# )

# assert first == same_process
# ```

#  Now we're defining the actual identity rule:

# ```
# Same PID
# +
# Same creation time
#         ↓
# Same process identity
# ```

#  while:

# ```
# Same PID
# +
# Different creation time
#         ↓
# Different process identity
# ```

#  That's why `assert` is valuable. **Printing shows you what happened; `assert` verifies what must be true.**

#  For Galaxy, I'd keep both during development: `assert` for correctness and a small `"test passed"` print for confirmation.
