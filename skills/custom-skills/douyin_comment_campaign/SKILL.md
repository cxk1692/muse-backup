# Douyin Comment Campaigns

## Confirm the account and the target list

- Confirm the logged in account matches the account the user confirmed for this campaign before you send the first comment.

- Stop and ask the user when the logged in account is different from the confirmed account instead of commenting from the wrong account.

- Build the target list from posts the user approved and remove every post already commented on in an earlier round.

- Check the topic of each target post against the campaign topic and remove any post about a different product with a similar name.

## Write a comment for that post only

- Read the target post before you write its comment and name the specific point you are answering in your first sentence.

- Write the second sentence so the code or link the user supplied follows naturally from that point instead of opening with a promotion.

- Vary the wording for every post and keep the tone colloquial and human instead of reusing one template across the round.

- Apply a new style rule only to comments not yet sent unless the user explicitly approves deleting and reposting a named comment already sent.

## Handle verification and skips without guessing

- Tell the user before the round starts that the first comment in a new browser session may trigger a code check even when an earlier session passed without one after the first check.

- Ask the user to stay available for that first code and batch the remaining comments after the check passes so the user is not asked for a code for every post.

- Skip a post when several accounts share the same name and you cannot identify the intended post with confidence.

- Replace a skipped post only with a backup post from the approved list and record the skip reason for the final report.

## Verify every comment and report the count

- Check each comment after you send it by confirming the comment count rose by one and the comment is visible under the confirmed account.

- Count only comments that pass that check and keep sent comments and skipped posts in separate totals.

- Report the sent list, the skipped list with reasons, and the verified total at the end of the round.

- Look up the post before any retry when a send result is uncertain instead of sending the same comment again.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Douyin](https://www.douyin.com/) for finding target posts and posting comments through `browser.browse`. Carry the approved target list and the comment written for each post into the browser task and verify the count and visibility for each comment there.

## Alternatives for better results

- Ask the user to post from their own phone when a campaign keeps triggering checks in a new browser session and the user prefers fewer checks over agent posting.

- Run a larger batch after the first check passes when the user approves it so one code check covers more comments.
