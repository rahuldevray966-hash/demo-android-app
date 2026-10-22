# Configure the pCloudy CI Workflow

What you need to set for `.github/workflows/main.yml` to run.

## 1. GitHub Secrets

**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
| --- | --- |
| `FIREBASE_SERVICE_ACCOUNT` | Google service-account JSON with access to Firebase App Distribution |
| `FIREBASE_PROJECT_NUMBER` | Firebase project number (digits only) |
| `FIREBASE_APP_ID` | Firebase Android app ID, e.g. `1:1234567890:android:abc123` |
| `PCLOUDY_EMAIL` | pCloudy account email |
| `PCLOUDY_ACCESS_KEY` | pCloudy API access key |

## 2. Target devices

File: `.github/config/devices.json`

```json
{
  "devices": [
    { "name": "Samsung_GalaxyS25_Android_15.0.0_d9af3", "enabled": true },
    { "name": "Samsung_GalaxyS22_Android_14.0.0_09b8b", "enabled": false }
  ]
}
```

- `name` must exactly match the pCloudy device full name. The **Fetch Target Devices** step log lists the names of the devices available right now.
- Only devices with `"enabled": true` are tested. At least one must be enabled.

## 3. Workflow settings

File: `.github/workflows/main.yml`

| Setting | Where | Default |
| --- | --- | --- |
| Android package name of the app identified by `FIREBASE_APP_ID` (Firebase console → Project settings → Your apps). Change both together. | top-level `env:` → `APP_PACKAGE` | `com.epam.mobitru` |
| Turns pCloudy's own performance data collection on or off | **Run Sequential Tests** step `env:` → `PCLOUDY_ENABLE_PERFORMANCE_DATA` | `"true"` |
| Branch that triggers a run | `on: push: branches:` | `main` |

The workflow can also be started manually from the **Actions** tab (`workflow_dispatch`).
