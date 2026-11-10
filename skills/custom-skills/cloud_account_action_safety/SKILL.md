# Cloud Browser Account Actions

## Warn before you act from a cloud browser

- Tell the user before you log in, post, comment, or change settings on a personal account from a cloud browser that the browser runs on a datacenter network and platforms may challenge, filter, or remove the action even when it looks accepted at first.

- Ask for explicit approval for that specific action after the warning and do not treat approval for an earlier action as approval for the next one.

- Stop and wait for the user when a code check, face check, or puzzle appears instead of retrying the action or asking for another code in the same session.

## Choose the safest route after a failure

- Switch to drafting only and ask the user to send from their own device when a cloud browser action was already filtered, removed, or blocked for this account or platform.

- Keep that draft only route in place until the user explicitly reauthorizes cloud browser action after a survival failure.

- Flag any scheduled work that would log in or post to the affected account and ask the user how to change it instead of letting it retry the blocked action on its own.

## Recheck visibility after a delay

- Recheck each sent post or comment after a delay and not only at send time, because filtering can remove an item that looked visible at first.

- Check visibility from the account view and from a logged out or public view when the platform allows it and record which view showed the item.

- Count only items still visible at the delayed recheck as surviving and report removed items as removed rather than as sent.

- Ask the user to confirm or remove an item in their own app when a recheck is uncertain instead of resending it from the cloud browser.

## Report the account state honestly

- Report the warning given, the approval received, the delayed recheck result, and the route chosen for the next action in the final report.

- Name any account action you did not take and why instead of reporting a round as complete when items were skipped, blocked, or removed.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Draft the exact text for the user to paste from their own device when speed matters less than survival of the post or comment.

- Send one test item and complete its delayed recheck before a larger round when an account has not yet survived a cloud browser action.