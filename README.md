Proof of concept, use rot13 on python src, load and decrypt using VM then `exec` it.

```py
# print('hello world')

if __name__ == "__main__":
    Vm(
      [4, 0, 20, 99, 101, 118, 97, 103, 40, 39, 117, 114, 121, 121, 98, 32, 106, 98, 101, 121, 113, 39, 41, 5, 0, 50, 20, 13]
    ).run()
```
