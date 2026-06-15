# Dashboard Layer

This document captures ideas for business dashboards that Codex or another
agentic harness can maintain almost autonomously for Jack's art business.

## Operating Principle

The dashboard should measure business momentum without making Jack feel judged by
productivity metrics. It should answer whether the business system is getting
healthier and whether finished art is being turned into available products.

Dashboards should support the August 1, 2026 goal: recurring or consistent
revenue from Jack's art or creative work. They should also keep an eye on Jack's
long-term goal of using art and creativity as the foundation for his career.

## Recommended First Implementation

Start with repo-local structured data and a generated Markdown dashboard.

Suggested files:

- `data/art_inventory.csv`
- `data/sales.csv`
- `data/expenses.csv`
- `data/experiments.csv`
- `data/checkins.csv`
- `docs/dashboard.md`

Why this path:

- Easy for Codex to create and maintain.
- Versioned in git.
- Works before there is a website or storefront.
- Can later generate HTML, charts, or Google Sheet views.
- Keeps the project memory in this repo.

## Core Dashboard Questions

The first dashboard should answer:

1. What finished art exists?
2. What can be sold right now?
3. Has anything sold?
4. What experiment are we running next?
5. What long-term career asset is being built?
6. What is the smallest next action?

## Dashboard Ideas

### North Star Dashboard

Purpose: track progress toward consistent creative revenue by August 1, 2026.

Metrics:

- Total revenue.
- Monthly revenue.
- Number of sales.
- Repeat buyers.
- Available pieces for sale.
- Products ready to sell.
- Interested supporters or email signups.
- Career-building assets created, such as catalog entries, portfolio pieces,
  product tests, buyer feedback, and reusable sales materials.
- Last business action completed.
- Current smallest next action.

This should be the main summary once data exists.

### Art Inventory Dashboard

Purpose: track Jack's creative assets and how close they are to being sellable.

Metrics:

- Finished pieces.
- Photographed or scanned pieces.
- Cataloged pieces.
- Originals available.
- Originals sold.
- Pieces eligible for prints, stickers, cards, zines, or digital products.
- Pieces missing title, price, photo, size, or status.

This is likely the most important early dashboard because the business starts
with finished work.

### Sales Dashboard

Purpose: understand actual money movement once sales begin.

Metrics:

- Gross revenue.
- Net revenue or profit estimate.
- Revenue by channel.
- Originals sold.
- Prints sold.
- Stickers/cards sold.
- Average sale price.
- Best-selling pieces/products.
- Buyer count.
- Repeat buyer count.

### Expense Dashboard

Purpose: keep small business costs visible.

Metrics:

- Printing costs.
- Packaging costs.
- Shipping costs.
- Platform fees.
- Art supplies.
- Gross revenue vs expenses.
- Estimated profit.

### Tiny Task Dashboard

Purpose: use Linear as the operating system without creating a guilt backlog.

Metrics:

- Tasks completed this week.
- Tasks ready now.
- Blocked tasks.
- Tasks assigned to Jack.
- Tasks assigned to Codex/agent.
- Tasks assigned to parent/guardian.
- Projects with no next action.
- Longest-stale task.

The dashboard should reward completed small tasks rather than accumulate huge
unfinished projects.

### Discord Accountability Dashboard

Purpose: understand whether Discord nudges are helping Jack take small,
productive steps toward art income.

Source:

- `data/discord_accountability_log.csv`
- `data/next_actions.csv`

Metrics:

- Prompts sent this week.
- Response rate.
- Best response hour.
- Voice used: gentle coach, direct teammate, or game challenge.
- Productive progress responses.
- Blockers named.
- Next steps identified.
- Ready next actions available for Jack.
- Follow-ups assigned to Jack, parent/guardian, Codex, or another agent.

This dashboard should evaluate the support system, not judge Jack. If response
rate drops or blockers increase, the next move is to soften the prompts, reduce
friction, or pick easier next actions.

### Experiment Dashboard

Purpose: track small business tests.

Example experiments:

- Show 5 pieces to 5 people.
- Test one $25 print.
- Post one available piece.
- Send available-work page to 10 trusted people.
- Compare interest in originals vs prints.

Metrics:

- Hypothesis.
- Action taken.
- Date started.
- Response count.
- Sales.
- Revenue.
- What was learned.
- Decision: continue, revise, stop, or pause.

### Audience Dashboard

Purpose: track supporter growth only if Jack wants public sharing.

Metrics:

- Email signups.
- Instagram/TikTok followers.
- Post engagement.
- Clicks to catalog/shop.
- People who asked about buying.
- Buyers from personal network vs public audience.

This should not be the main dashboard at first because audience metrics can be
demoralizing and may not reflect the quality of the art business.

## Implementation Options

### Option A: Repo-Local CSV and Markdown

Files live in the repo. Codex updates CSVs and regenerates
`docs/dashboard.md`.

Best for:

- First version.
- Durable memory.
- Low setup.
- Easy autonomous agent updates.

Tradeoff:

- Less visual than a web dashboard.

### Option B: Static HTML Dashboard

Codex generates a local static HTML dashboard from repo data files.

Best for:

- Nicer visuals.
- Charts.
- Filtering.
- Browser viewing.

Tradeoff:

- Slightly more maintenance than Markdown.

### Option C: Google Sheet Dashboard

Use Google Sheets for data entry and formulas.

Best for:

- Phone-friendly editing.
- Parent/guardian collaboration.
- Familiar spreadsheet interface.

Tradeoff:

- Less repo-native unless synced back.
- Depends on connector/auth setup.

### Option D: Linear-Powered Project Dashboard

Use Linear for project/task state, then have Codex summarize status back into
this repo.

Best for:

- Accountability.
- Stale task detection.
- Project planning.

Tradeoff:

- Linear is not ideal for art inventory, sales, expenses, or experiments unless
  those are mirrored elsewhere.

## Suggested Data Schemas

### `data/art_inventory.csv`

Columns:

- `id`
- `title`
- `created_date`
- `medium`
- `dimensions`
- `status`
- `original_price`
- `print_ready`
- `product_ideas`
- `image_path`
- `notes`

Suggested statuses:

- `draft`
- `finished`
- `cataloged`
- `available`
- `sold`
- `not_for_sale`
- `paused`

### `data/sales.csv`

Columns:

- `date`
- `item_id`
- `item_title`
- `product_type`
- `channel`
- `buyer_type`
- `gross_revenue`
- `fees`
- `shipping_charged`
- `shipping_cost`
- `net_revenue`
- `notes`

### `data/expenses.csv`

Columns:

- `date`
- `category`
- `vendor`
- `amount`
- `related_item_id`
- `notes`

### `data/experiments.csv`

Columns:

- `id`
- `name`
- `hypothesis`
- `start_date`
- `status`
- `action`
- `response_count`
- `sales_count`
- `revenue`
- `decision`
- `notes`

### `data/checkins.csv`

Columns:

- `date`
- `finished_art_count`
- `catalog_updates`
- `sales_updates`
- `blocked_items`
- `smallest_next_action`
- `notes`

## Agentic Maintenance Routine

On demand or weekly, Codex should:

1. Read repo data files.
2. Check Linear for relevant project/task status when needed.
3. Update inventory, sales, expenses, experiments, or check-ins.
4. Regenerate `docs/dashboard.md`.
5. Flag missing data.
6. Recommend 1-3 tiny next actions.

## Recommended First Dashboard Project

Project: Create Jack's Art Business Dashboard v1

Small tasks:

- Create starter `data/` CSV files.
- Add example rows or field definitions.
- Generate initial `docs/dashboard.md`.
- Add a dashboard update script if useful.
- Add a short dashboard update checklist.
- Connect dashboard next actions to Linear only after approval.

## Success Criteria

The dashboard layer is working if:

- It shows what art exists and what can be sold.
- It makes sales and expenses visible.
- It highlights missing catalog data.
- It identifies one small next action.
- It stays useful even when Jack has not created on a schedule.
- Codex can update it without rebuilding the system each time.
