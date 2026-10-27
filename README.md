# KwikQA for GitHub Actions

When your Playwright, Cypress, or WebdriverIO tests fail, this Action runs
[KwikQA](https://kwikqa.com) on the run:

- **Diagnosis.** It groups the failures by shared cause and diagnoses each group: who owns it (test
  code, application, or environment) and how strong the evidence is.
- **Failure report.** It writes `kwikqa-report.html`, with each group's evidence, and keeps it as
  an artifact of the run.
- **Summary.** It adds a summary to the run's page, and keeps it as one comment on the pull
  request. A re-run updates the comment instead of adding another.
- **Chat.** Optionally, it posts the run to Slack or Microsoft Teams through your own webhooks.

It never fails your build. Anything it can't publish is reported in the log and skipped.

## Usage

```yaml
permissions:
  contents: read
  pull-requests: write # only for the comment

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - run: npm ci && npx playwright install --with-deps
      - run: npx playwright test
      - if: failure()
        uses: kwikqa/action@v1
        with:
          kwikqa-token: ${{ secrets.KWIKQA_TOKEN }}
```

Playwright needs its JSON reporter, which KwikQA reads:

```ts
reporter: [["list"], ["json", { outputFile: "test-results/kwikqa-report.json" }]],
use: { trace: "retain-on-failure" },
```

Cypress and WebdriverIO setup, and every other report format KwikQA reads, are in the
[KwikQA guide](https://kwikqa.com/docs/).

## Inputs

| Input | Default | What it does |
| --- | --- | --- |
| `kwikqa-token` | none | A KwikQA CI token, from a secret. Create one at https://kwikqa.com/dashboard/account/. Without it, the run is analyzed locally and isn't diagnosed. |
| `github-token` | `github.token` | Writes the pull-request comment. The job needs `pull-requests: write`. |
| `report` | found | The test report, a file or a directory. |
| `framework` | none | For a JUnit report, the framework that wrote it: `playwright`, `cypress`, or `webdriverio`. |
| `working-directory` | `.` | The package that holds your tests. |
| `output` | `kwikqa-report.html` | Where to write the failure report, relative to `working-directory`. |
| `local` | `false` | `true` analyzes without asking a model, even with a token. |
| `notify` | `on-failure` | When to post to Slack and Teams: `on-failure` or `always`. |
| `slack-webhook-url` | none | A Slack incoming webhook's URL, from a secret. |
| `teams-webhook-url` | none | A Teams Workflows webhook's URL, from a secret. |
| `upload-report` | `true` | Keep the failure report as an artifact of the run. |
| `artifact-name` | `kwikqa-report` | The report artifact's name. Give each job of a matrix its own. |
| `version` | pinned | The kwikqa version to run. Each release of this Action names the one it was tested with. |

## Pull requests from forks

GitHub gives a fork's workflows no secrets and a read-only token. On such a pull request, KwikQA
analyzes the run locally, writes the report and the summary, and skips the comment. Don't switch to
`pull_request_target` to get the token: that event runs the fork's code with your repository's
secrets.

## Slack and Microsoft Teams

```yaml
        with:
          kwikqa-token: ${{ secrets.KWIKQA_TOKEN }}
          slack-webhook-url: ${{ secrets.KWIKQA_SLACK_WEBHOOK_URL }}
          teams-webhook-url: ${{ secrets.KWIKQA_TEAMS_WEBHOOK_URL }}
```

- **Slack.** Create an incoming webhook for the channel.
- **Teams.** In the channel, add the Workflows template "Post to a channel when a webhook request is
  received".

The message names the repository and branch, and links the pull request and the run. It lists each
failure group by its category, where it fails, its size, and its owner. It holds no error text,
evidence, or source code, because a channel is a wider audience than a build log. KwikQA keeps no
webhook, and never prints one.

## What leaves your runner

- **Your own systems.** The summary goes to your job, the comment to your pull request, and
  messages to your webhooks.
- **KwikQA.** With a token, KwikQA's diagnosis requests carry a redacted evidence packet, and each
  request's preview is printed in the job's log. The KwikQA service keeps account, usage, and
  request metadata only. Without a token, or with `local: true`, nothing goes to KwikQA.
- **The details.** See [Security and data handling](https://kwikqa.com/security/) and the
  [privacy policy](https://kwikqa.com/privacy/).

## Without the Action

The Action runs `npx kwikqa ci`, then uploads the report. Running those two steps yourself does the
same thing: see the [KwikQA guide](https://kwikqa.com/docs/).

## License

This repository's files are under the [MIT license](LICENSE). The Action downloads and runs the
`kwikqa` npm package, which is proprietary software licensed under its own end user license
agreement, the `LICENSE` file in that package. The KwikQA service is covered by the
[terms of service](https://kwikqa.com/terms/).
