# Branchdiff

A tool to let you more easily see the differences between commits in different
version of a patch series, when things have been reordered.

```
python3 ./branchdiff.py ./path/to/repo branch-v1 branch-v2 > out.html
```

Shows you the commits that are in one or the other of the branches, the
unchanged commits, and displays modified commits side by side.

Uses the commit summary to find commits that are the same.

## License

MIT
