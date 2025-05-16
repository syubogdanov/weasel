<h2 align="center">
    <img src="https://raw.githubusercontent.com/syubogdanov/weasel/refs/heads/main/branding/logo/weasel.png"
        alt="weasel-logo" height="128px" width="128px">
</h2>

[![weasel-version][shields/weasel/version]][github/homepage]
[![weasel-license][shields/github/license]][github/license]
[![python-version][shields/python/version]][github/homepage]
[![weasel-readthedocs][shields/readthedocs]][readthedocs/homepage]

> [!WARNING]
> The project is in the pre-alpha stage. Bugs may exist!

## Gettings Started

### Installation

#### Git

```bash
git clone https://github.com/syubogdanov/weasel.git
cd weasel/
poetry install
```

> Make sure you have *Python*, *Poetry* and *Git* installed.

#### Docker

```bash
git clone https://github.com/syubogdanov/weasel.git
cd weasel/
docker build --tag weasel .
```

> Make sure you have *Docker* installed.

### Usage

#### diff

For more, see the [documentation](readthedocs/homepage).

```bash
$ weasel diff --help
Usage: weasel diff [OPTIONS] SOURCE TARGET

  Compare files and highlight differences.

Options:
  --help  Show this message and exit.
```

#### info

For more, see the [documentation](readthedocs/homepage).

```bash
$ weasel info --help
Usage: weasel info [OPTIONS]

  Show the 'weasel' configuration.

Options:
  --help  Show this message and exit.
```

#### scan

For more, see the [documentation](readthedocs/homepage).

```bash
$ weasel scan --help
Usage: weasel scan [OPTIONS]

  Scan multiple files or repositories.

Options:
  --from-json FILE  Load from JSON.
  --from-toml FILE  Load from TOML.
  --from-yaml FILE  Load from YAML.
  --to-json TEXT    Write to JSON.
  --to-toml TEXT    Write to TOML.
  --to-yaml TEXT    Write to YAML.
  --help            Show this message and exit.
```

#### Examples

##### scan

Setting up the manifest file:

```yaml
tasks:
  - name: Dijkstra
    submissions:
      - name: Albert Einstein
        path: ./einstein/
      - name: Franz Kafka
        path: ./kafka.py
      - name: Hermann Karl Hesse
        github:
          user: hesse
          repo: dijkstra
      - name: Sigmund Freud
        bitbucket:
          user: freud
          repo: algorithms
          branch: dijkstra
```

Scan the tasks:

```bash
$ weasel scan --from-yaml=contest.yaml --to-yaml=report.yaml
weasel 0.0.0
------------

This may take a while...

Start:
- now:      2025-05-16 19:43:31.692+00:00

Finish:
- now:      2025-05-16 19:43:31.823+00:00

Reports:
- yaml:     report.yaml
```

See the report:

```bash
$ cat report.yaml
reviews:
- comparisons:
  - matches:
    - labels: []
      language: python
      probability: 1.0
      source: dijkstra.py
      target: dijkstra.py
    metrics:
      count: 1
      max: 1.0
      mean: 1.0
      median: 1.0
      min: 1.0
      nolie: 1.0
      p75: 1.0
      p90: 1.0
      p95: 1.0
      p99: 1.0
      std: 0.0
      var: 0.0
    source: Albert Einstein
    target: Franz Kafka
  - ...
```

## License

MIT License, Copyright (c) 2025 Sergei Y. Bogdanov. See [LICENSE][github/license] file.

<!-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -->

[github/homepage]: https://github.com/syubogdanov/weasel
[github/license]: https://github.com/syubogdanov/weasel/tree/main/LICENSE

[readthedocs/homepage]: https://weasel.readthedocs.io/

[shields/github/license]: https://img.shields.io/github/license/syubogdanov/weasel?style=flat&color=green
[shields/python/version]: https://img.shields.io/badge/python-3.13-green
[shields/readthedocs]: https://img.shields.io/readthedocs/weasel?style=flat&color=green
[shields/weasel/version]: https://img.shields.io/badge/version-0.0.0-green
