**Run your Mailchimp marketing operations through AI.**

A Model Context Protocol (MCP) server that exposes Mailchimp's Marketing API for reading and managing automations, audiences, campaigns, templates, landing pages, and e-commerce data.


## Overview

The MewCP Mailchimp MCP Server provides authenticated access to the Mailchimp Marketing API:

- Inspect classic automation workflows, their individual emails, and the subscribers queued in each email's send queue
- List and read audiences (lists) and campaigns, including full campaign performance reports
- Manage Classic templates and folders, and inspect landing pages and their published HTML content
- Query connected e-commerce stores, products, and orders — including orders attributed to a specific campaign

Perfect for:

- AI assistants that need to read or manage Mailchimp marketing data
- Automating campaign and automation performance reporting
- Building tools that connect Mailchimp audience, campaign, and e-commerce data to other systems


## Tools

### Automations

<details>
<summary><code>list_automations</code> — List all classic automation workflows</summary>

Get a summary of an account's classic automations with optional filtering and pagination

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of records to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
- `fields` (string, optional, default: null) — Comma-separated list of fields to return
- `exclude_fields` (string, optional, default: null) — Comma-separated list of fields to exclude
- `before_create_time` (string, optional, default: null) — Restrict to automations created before this time (ISO 8601: 2015-10-21T15:41:36+00:00)
- `since_create_time` (string, optional, default: null) — Restrict to automations created after this time (ISO 8601: 2015-10-21T15:41:36+00:00)
- `before_start_time` (string, optional, default: null) — Restrict to automations started before this time (ISO 8601: 2015-10-21T15:41:36+00:00)
- `since_start_time` (string, optional, default: null) — Restrict to automations started after this time (ISO 8601: 2015-10-21T15:41:36+00:00)
- `status` (string, optional, default: null) — Filter by status: 'save', 'paused', or 'sending'
```

**Output `data` schema:**

```typescript
{
  automations: {
    id: string | null;
    create_time: string | null;
    start_time: string | null;
    status: string | null;
    emails_sent: number | null;
    recipients: {
      list_id: string | null;
      store_id: string | null;
    } | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_automation_info</code> — Get details of a specific automation workflow</summary>

Get detailed information about a specific automation workflow by ID

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the Automation workflow
- `fields` (string, optional, default: null) — Comma-separated list of fields to return
- `exclude_fields` (string, optional, default: null) — Comma-separated list of fields to exclude
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  create_time: string | null;
  start_time: string | null;
  status: string | null;
  emails_sent: number | null;
  recipients: {
    list_id: string | null;
    store_id: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>list_automated_emails</code> — List emails in an automation workflow</summary>

Get a summary of the emails in a classic automation workflow

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the Automation workflow
```

**Output `data` schema:**

```typescript
{
  emails: {
    id: string | null;
    workflow_id: string | null;
    position: number | null;
    status: string | null;
    emails_sent: number | null;
    send_time: string | null;
    content_type: string | null;
    settings: {
      subject_line: string | null;
      title: string | null;
      from_name: string | null;
      reply_to: string | null;
    } | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_workflow_email_info</code> — Get details of a specific automation email</summary>

Get detailed information about a specific email in an automation workflow

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the Automation workflow
- `workflow_email_id` (string, required) — The unique ID of the Automation workflow email
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  workflow_id: string | null;
  position: number | null;
  status: string | null;
  emails_sent: number | null;
  send_time: string | null;
  content_type: string | null;
  settings: {
    subject_line: string | null;
    title: string | null;
    from_name: string | null;
    reply_to: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>list_automated_email_subscribers</code> — List subscribers queued for an automation email</summary>

Get information about subscribers queued to receive a specific automation email

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the Automation workflow
- `workflow_email_id` (string, required) — The unique ID of the Automation workflow email
```

**Output `data` schema:**

```typescript
{
  queue: {
    id: string | null;
    workflow_id: string | null;
    email_id: string | null;
    list_id: string | null;
    email_address: string | null;
    next_send: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_automated_email_subscriber</code> — Get a specific subscriber in an automation email queue</summary>

Get detailed information about a specific subscriber to an automation email queue

**Inputs:**
```
- `workflow_id` (string, required) — The unique ID of the Automation workflow
- `workflow_email_id` (string, required) — The unique ID of the Automation workflow email
- `subscriber_hash` (string, required) — The MD5 hash of the lowercase version of the subscriber's email address
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  workflow_id: string | null;
  email_id: string | null;
  list_id: string | null;
  email_address: string | null;
  next_send: string | null;
}
```

</details>


### Audiences

<details>
<summary><code>list_audience</code> — List all audiences (lists)</summary>

Get information about all lists (audiences) in the account

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  lists: {
    id: string | null;
    web_id: number | null;
    name: string | null;
    date_created: string | null;
    stats: {
      member_count: number | null;
      unsubscribe_count: number | null;
      open_rate: number | null;
      click_rate: number | null;
    } | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_list_info</code> — Get details of a specific audience</summary>

Get detailed information about a specific list (audience) in your Mailchimp account

**Inputs:**
```
- `list_id` (string, required) — The unique ID for the list
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  web_id: number | null;
  name: string | null;
  date_created: string | null;
  stats: {
    member_count: number | null;
    unsubscribe_count: number | null;
    open_rate: number | null;
    click_rate: number | null;
  } | null;
}
```

</details>


### Campaigns

<details>
<summary><code>list_campaigns</code> — List all campaigns</summary>

Get all campaigns in an account

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  campaigns: {
    id: string | null;
    web_id: number | null;
    type: string | null;
    create_time: string | null;
    status: string | null;
    emails_sent: number | null;
    send_time: string | null;
    recipients: {
      list_id: string | null;
      segment_text: string | null;
      recipient_count: number | null;
    } | null;
    settings: {
      subject_line: string | null;
      title: string | null;
      from_name: string | null;
      reply_to: string | null;
    } | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_campaign_info</code> — Get details of a specific campaign</summary>

Get detailed information about a specific campaign

**Inputs:**
```
- `campaign_id` (string, required) — The unique ID for the campaign
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  web_id: number | null;
  type: string | null;
  create_time: string | null;
  status: string | null;
  emails_sent: number | null;
  send_time: string | null;
  recipients: {
    list_id: string | null;
    segment_text: string | null;
    recipient_count: number | null;
  } | null;
  settings: {
    subject_line: string | null;
    title: string | null;
    from_name: string | null;
    reply_to: string | null;
  } | null;
}
```

</details>


<details>
<summary><code>list_campaign_reports</code> — List all campaign reports</summary>

Get all campaign reports with performance metrics

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of reports to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
- `type` (string, optional, default: null) — Filter by campaign type: 'regular', 'plaintext', 'absplit', 'rss', or 'variate'
```

**Output `data` schema:**

```typescript
{
  reports: {
    id: string | null;
    campaign_title: string | null;
    type: string | null;
    list_id: string | null;
    list_name: string | null;
    emails_sent: number | null;
    send_time: string | null;
    opens: {
      opens_total: number | null;
      unique_opens: number | null;
      open_rate: number | null;
    } | null;
    clicks: {
      clicks_total: number | null;
      unique_clicks: number | null;
      click_rate: number | null;
    } | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_campaign_report</code> — Get report for a specific campaign</summary>

Get detailed report for a specific sent campaign

**Inputs:**
```
- `campaign_id` (string, required) — The unique ID for the campaign
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  campaign_title: string | null;
  type: string | null;
  list_id: string | null;
  list_name: string | null;
  emails_sent: number | null;
  send_time: string | null;
  opens: {
    opens_total: number | null;
    unique_opens: number | null;
    open_rate: number | null;
  } | null;
  clicks: {
    clicks_total: number | null;
    unique_clicks: number | null;
    click_rate: number | null;
  } | null;
}
```

</details>


### Landing Pages

<details>
<summary><code>list_landing_pages</code> — List all landing pages</summary>

Get all landing pages in your account

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of landing pages to return (max: 1000)
- `sort_field` (string, optional, default: null) — Sort by: 'created_at' or 'updated_at'
- `sort_dir` (string, optional, default: null) — Sort direction: 'ASC' or 'DESC'
```

**Output `data` schema:**

```typescript
{
  landing_pages: {
    id: string | null;
    name: string | null;
    title: string | null;
    status: string | null;
    url: string | null;
    store_id: string | null;
    list_id: string | null;
    template_id: number | null;
    created_at: string | null;
    published_at: string | null;
    updated_at: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_landing_page_info</code> — Get details of a specific landing page</summary>

Get detailed information about a specific landing page by ID

**Inputs:**
```
- `page_id` (string, required) — The unique ID for the landing page
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  title: string | null;
  status: string | null;
  url: string | null;
  store_id: string | null;
  list_id: string | null;
  template_id: number | null;
  created_at: string | null;
  published_at: string | null;
  updated_at: string | null;
}
```

</details>


<details>
<summary><code>get_landing_page_content</code> — Get the HTML content of a landing page</summary>

Get the HTML content for a specific landing page

**Inputs:**
```
- `page_id` (string, required) — The unique ID for the landing page
```

**Output `data` schema:**

```typescript
{
  html: string | null;
}
```

</details>


### Templates

<details>
<summary><code>list_template_folders</code> — List all template folders</summary>

Get all folders used to organize templates

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of folders to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
```

**Output `data` schema:**

```typescript
{
  folders: {
    id: string | null;
    name: string | null;
    count: number | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>add_template_folder</code> — Create a new template folder</summary>

Create a new template folder

**Inputs:**
```
- `name` (string, required) — The name of the folder
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  count: number | null;
}
```

</details>


<details>
<summary><code>list_templates</code> — List all templates</summary>

Get all templates in your account

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of templates to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
- `type` (string, optional, default: null) — Filter by type: 'user', 'base', or 'gallery'
- `content_type` (string, optional, default: null) — Filter by content type: 'html', 'template', or 'multichannel'
```

**Output `data` schema:**

```typescript
{
  templates: {
    id: number | null;
    type: string | null;
    name: string | null;
    date_created: string | null;
    date_edited: string | null;
    active: boolean | null;
    folder_id: string | null;
    thumbnail: string | null;
    share_url: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_template_info</code> — Get details of a specific template</summary>

Get detailed information about a specific template by ID

**Inputs:**
```
- `template_id` (string, required) — The unique ID for the template
```

**Output `data` schema:**

```typescript
{
  id: number | null;
  type: string | null;
  name: string | null;
  date_created: string | null;
  date_edited: string | null;
  active: boolean | null;
  folder_id: string | null;
  thumbnail: string | null;
  share_url: string | null;
  html: string | null;
}
```

</details>


<details>
<summary><code>add_template</code> — Create a new template</summary>

Create a new Classic template for the account. It supports Mailchimp Template Language

**Inputs:**
```
- `name` (string, required) — The name of the template
- `html` (string, required) — The raw HTML for the template. Supports Mailchimp Template Language
- `folder_id` (string, optional, default: null) — The ID of the folder to place the template in
```

**Output `data` schema:**

```typescript
{
  id: number | null;
  type: string | null;
  name: string | null;
  date_created: string | null;
  date_edited: string | null;
  active: boolean | null;
  folder_id: string | null;
  thumbnail: string | null;
  share_url: string | null;
}
```

</details>


<details>
<summary><code>update_template</code> — Update an existing template</summary>

Updates the name, HTML, or folder of an existing Classic template. This overwrites the current name and HTML with the values you provide (folder_id is only changed if given) — the original state is not stored by the API after the call. The response includes both the before and after state so you have a full record of what changed.

**Inputs:**
```
- `template_id` (string, required) — The unique ID for the template
- `name` (string, required) — The name of the template
- `html` (string, required) — The raw HTML for the template. Supports Mailchimp Template Language
- `folder_id` (string, optional, default: null) — The ID of the folder to move the template to
```

**Output `data` schema:**

```typescript
{
  id: number | null;
  type: string | null;
  name: string | null;
  date_created: string | null;
  date_edited: string | null;
  active: boolean | null;
  folder_id: string | null;
  thumbnail: string | null;
  share_url: string | null;
  before: {
    id: number | null;
    type: string | null;
    name: string | null;
    date_created: string | null;
    date_edited: string | null;
    active: boolean | null;
    folder_id: string | null;
    thumbnail: string | null;
    share_url: string | null;
    html: string | null;
  };
  after: {
    id: number | null;
    type: string | null;
    name: string | null;
    date_created: string | null;
    date_edited: string | null;
    active: boolean | null;
    folder_id: string | null;
    thumbnail: string | null;
    share_url: string | null;
    html: string | null;
  };
}
```

</details>


### E-commerce

<details>
<summary><code>list_stores</code> — List all e-commerce stores</summary>

Get information about all e-commerce stores in the account

**Inputs:**
```
- `count` (int, optional, default: 10) — Number of stores to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
```

**Output `data` schema:**

```typescript
{
  stores: {
    id: string | null;
    list_id: string | null;
    name: string | null;
    platform: string | null;
    domain: string | null;
    currency_code: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_store_info</code> — Get details of a specific e-commerce store</summary>

Get detailed information about a specific e-commerce store

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  list_id: string | null;
  name: string | null;
  platform: string | null;
  domain: string | null;
  currency_code: string | null;
}
```

</details>


<details>
<summary><code>list_products</code> — List products in an e-commerce store</summary>

Get information about all products in a specific e-commerce store

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `count` (int, optional, default: 10) — Number of products to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
```

**Output `data` schema:**

```typescript
{
  products: {
    id: string | null;
    title: string | null;
    handle: string | null;
    url: string | null;
    type: string | null;
    vendor: string | null;
    image_url: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_product_info</code> — Get details of a specific product</summary>

Get detailed information about a specific product in an e-commerce store

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `product_id` (string, required) — The unique ID for the product
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  title: string | null;
  handle: string | null;
  url: string | null;
  type: string | null;
  vendor: string | null;
  image_url: string | null;
}
```

</details>


<details>
<summary><code>list_store_orders</code> — List orders in an e-commerce store</summary>

Get information about all orders in a specific e-commerce store

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `count` (int, optional, default: 10) — Number of orders to return (max: 1000)
- `offset` (int, optional, default: 0) — Number of records to skip for pagination
- `customer_id` (string, optional, default: null) — Restrict results to orders made by a specific customer
- `campaign_id` (string, optional, default: null) — Restrict results to orders with a specific campaign ID
```

**Output `data` schema:**

```typescript
{
  orders: {
    id: string | null;
    customer: {
      id: string | null;
      email_address: string | null;
    } | null;
    campaign_id: string | null;
    financial_status: string | null;
    fulfillment_status: string | null;
    currency_code: string | null;
    order_total: number | null;
    processed_at_foreign: string | null;
  }[];
  total_items: number | null;
}
```

</details>


<details>
<summary><code>get_order_info</code> — Get details of a specific order</summary>

Get detailed information about a specific order in an e-commerce store

**Inputs:**
```
- `store_id` (string, required) — The unique ID for the store
- `order_id` (string, required) — The unique ID for the order
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  customer: {
    id: string | null;
    email_address: string | null;
  } | null;
  campaign_id: string | null;
  financial_status: string | null;
  fulfillment_status: string | null;
  currency_code: string | null;
  order_total: number | null;
  processed_at_foreign: string | null;
}
```

</details>


### System

<details>
<summary><code>health_check</code> — Check Mailchimp API connectivity</summary>

Check Mailchimp API connectivity

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  health_status: string | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "ERROR_CODE", "message": "description", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Pagination Parameters</strong></summary>

- `count` — Number of records to return per request (default: 10, max: 1000)
- `offset` — Number of records to skip; use with `count` to page through results

</details>

<details>
<summary><strong>Field Filtering</strong></summary>

`list_automations` and `get_automation_info` support field filtering to shrink the response payload.

- `fields` — Comma-separated list of response fields to include
- `exclude_fields` — Comma-separated list of response fields to omit

**Example:**
```
fields: "automations.id,automations.status"
exclude_fields: "_links"
```

</details>

<details>
<summary><strong>Date/Time Format</strong></summary>

All datetime parameters use ISO 8601 format:

```
Format: YYYY-MM-DDTHH:MM:SS+HH:MM
Example: 2015-10-21T15:41:36+00:00
```

</details>

<details>
<summary><strong>Subscriber Hash</strong></summary>

The `subscriber_hash` parameter used by `get_automated_email_subscriber` is the MD5 hash of the subscriber's lowercase email address.

```
Input: user@example.com → lowercase → user@example.com
Hash: md5("user@example.com") → b58996c504c5638798eb6b511e6f49af
```

</details>

<details>
<summary><strong>Server Prefix</strong></summary>

Every request is signed with your Mailchimp OAuth access token plus a `server_prefix` credential extra (e.g. `us21`) — the data center your Mailchimp account lives on. This is not part of any tool's inputs; it is stored on the credential itself and read automatically for every call.

Find it in the URL you use to log in to Mailchimp: `https://usXX.admin.mailchimp.com` — `usXX` is your `server_prefix`.

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers, or the linked credential is missing its `server_prefix` extra
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that the credential's extras include a valid `server_prefix` matching your Mailchimp account's data center
  3. Check the OAuth token has not expired — reconnect in your MewCP account if needed

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Mailchimp credential linked to your account, or the credential has no `server_prefix` stored
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Mailchimp account via OAuth — this stores both the access token and your account's `server_prefix`
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values (e.g. `count` must be an integer)

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use the correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Mailchimp API Error</strong></summary>

- **Cause:** Upstream Mailchimp API returned an error
- **Solution:**
  1. Check the [Mailchimp Status Page](https://status.mailchimp.com) for service issues
  2. Verify your OAuth credential has the required permissions for the requested resource
  3. Review the error message returned in the response for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Mailchimp Marketing API Documentation](https://mailchimp.com/developer/marketing/docs/fundamentals/)** — Official API reference
- **[Mailchimp API Reference](https://mailchimp.com/developer/marketing/api/)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
