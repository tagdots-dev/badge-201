# badge-test

## 😎 Why you need setup-badge?
**setup-badge** uses your inputs to create a JSON endpoint which is provided to [shields.io endpoint badge](https://shields.io/badges/endpoint-badge) to format the badge.  My primary motivation is to use endpoint badge to pick up dynamic data.  For instance, after running code coverage in _action_, my badge needs to display the latest code coverage percentage.

<br>

## ⭐ How setup-badge works

1. You run **setup-badge** with your inputs.
1. **setup-badge** uses the default _template.json_ to add/update a json file with your inputs.
1. **setup-badge** makes a commit to your branch and push the branch to remote.
1. **endpoint-badge** is constructed with shields.io endpoint and your json file as an endpoint.

![How It Works](https://raw.githubusercontent.com/tagdots-dev/badge-test/refs/heads/main/assets/setup-badge.png)

<br>


## 🔧 setup-badge command line inputs

| Input | Description | Default | Notes |
|-------|-------------|----------|----------|
| `badge-name` | JSON endpoint filename | `badge` | JSON endpoint filename |
| `badge-file-src` | Badge JSON file template | `src/setup-badge/default/template.json` | JSON endpoint template file |
| `branch-name` | Branch to hold JSON endpoint | `badges` | you can use a single branch to hold multiple JSON endpoint files |
| `remote-name` | Git remote source branch | `origin` | you should leave it as-is in general |
| `badge-style` | Badge style | `flat` | other options: `flat-square`, `plastic`, `for-the-badge`, `social` |
| `label` | Left side text | `demo` | - |
| `label-color` | Left side background color | `2e2e2e` | hex color |
| `message` | Right side text | `no status` | you can pass dynamic operating result here |
| `message-color` | Right side background color | `2986CC` | hex color |
| `gitconfig-name` | Git config user name | `Mona Lisa` | you need this option for GitHub action |
| `gitconfig-email` | Git config user email | `mona.lisa@example.com` | you need this option for GitHub action |

<br>

### Use Case 1️⃣ - running on GitHub action
Please visit our GitHub action ([setup-badge-action](https://github.com/marketplace/actions/setup-badge-action)) on the `GitHub Marketplace`.

<br>

### Use Case 2️⃣ - running locally on your computer

### 🔆 Install setup-badge

In the command-line examples below, we use a GitHub project named `badge-test`.

We will first install **setup-badge** in a virtual environment named after the project.  Next, we will run **setup-badge** with different options and show the results.

```
~/work/badge-test $ workon badge-test
(badge-test) ~/work/badge-test $ pip install -U setup-badge
```

<br>

### 🔍 Using setup-badge

🏃 _**Run to show command line usage and options**_: `--help`

```
(badge-test) ~/work/badge-test $ setup-badge --help
Usage: setup-badge [OPTIONS]

Options:
  --badge-name TEXT       default: badge
  --badge-file-src TEXT   default: src/pkg_18604/default/template.json
  --badge-branch TEXT     default: badges
  --remote-name TEXT      default: origin
  --badge-style TEXT      default: flat (flat, flat-square, plastic, for-the-badge, social)
  --label TEXT            default: demo (badge left side text)
  --label-color TEXT      default: 2e2e2e (badge left side hex color)
  --message TEXT          default: no status (badge right side text)
  --message-color TEXT    default: 2986CC (badge right side hex color)
  --gitconfig-name TEXT   default: Mona Lisa
  --gitconfig-email TEXT  default: mona.lisa@example.com
  --ci-cleanup BOOLEAN    default: False
  --version               Show the version and exit.
  --help                  Show this message and exit.
```

<br>

🏃 _**Run default inputs**_

When **setup-badge** runs with default inputs, it will create an

1. create a `badges` branch.
1. create a `badge.json` file from the inputs and `template.json`.
1. create a commit and push `badge.json` file to `badges` branch.
1. produce an `endpoint badge`.

```
(badge-test) ~/work/badge-test $ setup-badge
🚀 Starting to create a badge.json in branch (badges)...

✅ checkout branch (badges) locally
✅ validated inputs from command line options
✅ created badge.json from template.json
✅ found unstaged changes ready to stage, commit, and push to origin
✅ pushed commit (f9c751c) to remote with branch (badges)

🎉 Endpoint Badge: ![badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tagdots-dev/badge-test/refs/heads/badges/badges/badge.json)
```

<br>

## 🔔 How to use Endpoint Badge?
Choose one of the following options and add to README file.

**clickable to your JSON endpoint**<br>![click-to-json-endpoint](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tagdots-dev/badge-201/refs/heads/initial-release/badges/click-to-json-endpoint.json)

```
![click-to-json-endpoint](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tagdots-dev/badge-201/refs/heads/initial-release/badges/click-to-json-endpoint.json)
```

**clickable to your custom URL**<br>
[![click-to-custom-url](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tagdots-dev/badge-201/refs/heads/initial-release/badges/click-to-custom-url.json)](https://www.github.com/tagdots-dev/badge-test)

```
[![click-to-custom-url](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tagdots-dev/badge-201/refs/heads/initial-release/badges/click-to-custom-url.json)](https://www.github.com/tagdots-dev/badge-test)
```

<br><br>

## 😕  Troubleshooting

Open an [issue][issues]

<br>

## 🙏  Contributing

Pull requests and stars are always welcome.  For pull requests to be accepted on this project, you should follow [PEP8][pep8] when creating/updating Python codes.

See [Contributing][contributing]

<br>

## 📚 References

[Shields.io Endpoint Badge](https://shields.io/badges/endpoint-badge)

[Hex Color](https://www.color-hex.com/)

[How to fork a repo](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

<br>

[contributing]: https://github.com/tagdots-dev/badge-test/blob/main/CONTRIBUTING.md
[issues]: https://github.com/tagdots-dev/badge-test/issues
[pep8]: https://google.github.io/styleguide/pyguide.html
