"""
Update enterpret-modules.json with data from the markdown analysis document.

Changes applied:
1. Move subtheme entries (rank > 15) from flat top_complaints.themes into deep_dive.subthemes
2. Add short "title" labels to priority_recommendations (previously truncated/wrong)
3. Add "url" field to nps_detractor_comments (Enterpret record URLs from markdown)
4. Add verbatim quotes to top_complaints.quotes, top_improvements.quotes, praise.quotes
"""

import json, re

BASE_URL = "https://dashboard.enterpret.com/auditboard/record/"

# ── 1. Priority recommendation short titles ───────────────────────────────────
PRIORITY_TITLES = {
    "dashboards": [
        "Fix the Sigma migration fallout",
        "Build a native unified cross-module dashboard",
        "Implement row-level / audience-specific permissions",
        "Launch a custom views / data flexibility program",
        "Formalize BI/API integration as a first-class capability",
    ],
    "risks": [
        "Deliver true bidirectional Audit–Risk integration",
        "Build a configurable, formula-driven risk scoring engine",
        "Redesign the Entity Risk onboarding and conceptual framework",
        "Address the ROI/adoption gap for existing RiskOversight customers",
        "Add KPI/KRI historical trend data and point-in-time snapshots",
    ],
    "issues": [
        "Make issue form customization self-service",
        "Implement governed multi-level action plan close workflow",
        "Fix role-based permissions model for Issue Management stakeholders",
        "Clarify and simplify the Standard vs. Custom Issues tier boundary",
        "Build automated escalation and notification engine",
    ],
    "opsaudit": [
        "Invest in OpsAudit fieldwork UX as a dedicated improvement program",
        "Automate the audit planning lifecycle end-to-end",
        "Deliver native parent-child auditable entity hierarchy support",
        "Simplify the tier/permissions boundary communication in-product",
        "Commit to a community idea delivery cadence for OpsAudit",
    ],
    "workstream": [
        "Redesign the permissions model for Workstream",
        "Build configurable reminder/notification engine",
        "Enable parallel/conditional approval routing",
        "Expand survey/form question types and conditional logic",
        "Deliver the Jira integration as sold",
    ],
    "settings": [
        "Fix the permission inheritance security vulnerability immediately",
        "Redesign the Platform Admin role to be a true superadmin",
        "Build a permissions explainer/wizard in-product",
        "Overhaul Core User vs. Stakeholder licensing communication",
        "Improve SSO/SCIM reliability and document the configuration",
    ],
    "esg": [
        "Build automated source data connectors for common ESG data systems",
        "Deliver CSRD double materiality assessment support",
        "Build a comprehensive, auto-updating ESG framework library",
        "Simplify ESG admin configuration and bulk data management",
        "Develop an ESG-specific onboarding and consulting program",
    ],
    "tprm": [
        "Automate rule-based vendor assessment initiation and intake",
        "Invest in AI-assisted questionnaire completion as a flagship TPRM differentiator",
        "Move multi-sign-off approval workflows out of higher tiers",
        "Build a TPRM adoption program with program design guidance",
        "Fix reliability issues and change bug support culture",
    ],
    "narratives": [
        "Fix AI Generate Narrative silent failure",
        "Fix Lucidchart sync reliability",
        "Clarify and simplify the Narrative type configuration for AI enablement",
        "Add in-platform inline commenting/annotation for narrative review",
        "Establish dedicated Narratives taxonomy for signal tracking",
    ],
    "regcomply": [
        "Clarify and decouple the RegComply vs. CrossComply positioning",
        "Build horizon scanning for proposed regulations",
        "Expand regulatory content to non-FinServ industries and international jurisdictions",
        "Automate change applicability determination with AI",
        "Build bulk mapping tools for regulation-to-control/policy/risk linkage",
    ],
    "exceptions": [
        "Build a native exception management dashboard",
        "Enable multiple templates and configurable workflows",
        "Fix the policy-exception to issue creation bug",
        "Add bulk approval/status-update tooling for migration use cases",
        "Create end-user training for approvers and reviewers",
    ],
    "integrations": [
        "Fix SSO/SCIM as the #1 integration support burden",
        "Deliver Google Drive / Google Workspace integration",
        "Make Jira integration work as promised",
        "Invest in developer enablement",
        "Expand native connectors for ERP and HR systems",
    ],
    "automations": [
        "Establish an Automations/Accelerate taxonomy node in the Knowledge Graph",
        "Fix the API rate limit architecture for Accelerate + SCIM coexistence",
        "Simplify the AI tier boundary communication",
        "Build guided automation setup for top 5 use cases",
        "Develop ROI calculator and BVA tooling to accelerate Accelerate sales",
    ],
    "inventory": [
        "Deliver native parent-child auditable entity hierarchy",
        "Remove the single-inventory-type restriction per entity",
        "Enable self-service bulk update of auditable entities",
        "Build CMDB/HRIS auto-sync for asset and personnel inventories",
        "Rename 'Auditable Entities' to plain-language terminology",
    ],
    "ai-governance": [
        "Establish AI Governance taxonomy node in Knowledge Graph",
        "Prioritize shadow AI discovery as P1 for product roadmap",
        "Deliver EU AI Act article-level framework mapping",
        "Accelerate ServiceNow/Jira integration delivery",
        "Develop an 'AI Governance Quick Start' program for early-stage customers",
    ],
    "files": [
        "Fix file upload reliability (stuck at 100%)",
        "Investigate and urgently resolve the periodic deletion of core files engineering issue",
        "Add subfolder hierarchy to the Files toolkit",
        "Enable self-service document template customization",
        "Add visible review/signoff status to the Files screen",
    ],
    "timesheets": [
        "Restore full Timesheets dashboard parity with pre-Sigma PowerBI version",
        "Build timesheet locking with approval workflow",
        "Add UID to OpsAudit Timesheets",
        "Build HRIS integration for PTO/time-off sync",
        "Deliver the New OpsAudit Global Timesheet Dashboard",
    ],
    "asq": [
        "Establish ASQ taxonomy in the Knowledge Graph",
        "Fix questionnaire bundle deletion bug",
        "Pre-populate ASQ with common framework knowledge bases (SIG, CAIQ, SOC 2, ISO 27001)",
        "Expand questionnaire format support (Word, PDF) beyond Excel",
        "Build AI-assisted response quality feedback loop",
    ],
    "itrm": [
        "Fix ITRM dashboard data population (Risk Insights + Mitigation Plans showing zero data)",
        "Build automated CMDB sync for IT asset inventory",
        "Simplify asset-risk entity relationship mapping with guided setup",
        "Deliver an ITRM onboarding accelerator program",
        "Clarify and deliver Cyber Risk Quantification capabilities",
    ],
}

# ── 2. NPS detractor comment URLs (one list per module, in order matching existing comments) ─────
NPS_URLS = {
    "dashboards": [
        "5a580ff2-4f9e-5a1c-9776-5f5268f9d655",
        "71cc9114-8ea2-5427-80fa-c75517922cf2",
        "1fe4090b-2083-5f92-bbff-1fa49e657924",
        "25a47f10-89d0-57d2-a749-88fedffc99ab",
        "5e36a589-a4db-5131-8eda-9760e0f4caf7",
        "b398c64e-d3c4-59ec-b6fb-8689668f1bf5",
        "504c280d-9912-5922-80ed-4cb513431e09",
        "d6a2df67-795d-58f9-936f-5c5d8cc022a5",
        "c8c3320f-be76-5754-920e-1e997293e58e",
    ],
    "risks": [
        "2b4e5716-12fe-581b-b585-732776e7deec",
        "469068b5-4617-5660-8ff6-4407be7d4b2b",
        "f1c24bf3-d95f-5372-a687-38607e800a3b",
        "78678dd5-ea94-57d3-9d4e-588757a3a0fd",
        "5e36a589-a4db-5131-8eda-9760e0f4caf7",
    ],
    "issues": [
        "20c6ce76-629a-509c-b939-d79504c0601c",
        "09469671-ed99-5768-81e7-ea1a2dc05dd5",
        "539bb233-84c4-59e9-9acb-3f384178adbc",
        "aef8ff93-58cf-52ef-a21f-1078e3566bab",
        "21715cf9-8360-5874-b642-b3e496ff3e1f",
    ],
    "opsaudit": [
        "2b4e5716-12fe-581b-b585-732776e7deec",
        "8ef495eb-6a57-599d-8487-8c8f219d0999",
        "25c386b8-31b5-52d4-aed2-89a34d45e67f",
        "8cbb73be-0fa9-5e83-a98e-df154c1fbc1c",
        "c51ce762-18e4-5c50-9f0a-bc4b54e5d88f",
        "804046c1-67a2-5528-b7b5-7dfed91c0239",
    ],
    "workstream": [
        "8ef495eb-6a57-599d-8487-8c8f219d0999",
        "55a4bf49-7dbc-5862-b686-203ed97ab581",
        "60d2bbb5-df5a-58e2-98c5-fa72e5f277b4",
        "125237f5-be09-5426-a9cc-e4542cd8d87f",
        "a7f385e8-c1f7-58d8-baba-7b7bed488172",
    ],
    "settings": [
        "57ab85ba-425b-5f4a-b5a3-00e0360dd58a",
        "df0c8f59-20b2-54f4-a288-1d5fd31b6732",
        "ed1520e8-b134-5ac2-90b7-c638a0852a74",
        "fd63cf86-f630-56fe-91a6-e07ae986db11",
        "dfc191b1-5b80-547a-944b-10e7d3d2bc70",
    ],
    "esg": [
        "53550820-4574-56bf-80d9-835e091af30a",
        "a08391d4-6660-5e66-a564-4baa7ae903d6",
    ],
    "tprm": [
        "db1b3c59-04ec-50cf-b851-7873f16f46d1",
        "a6765a1a-3f81-5e06-a0ab-00e810422f18",
    ],
    "exceptions": [
        "fcdc0c75-9d30-5145-93e6-661bc59edb88",
    ],
    "integrations": [
        "8ef495eb-6a57-599d-8487-8c8f219d0999",
        "df0c8f59-20b2-54f4-a288-1d5fd31b6732",
        "60d2bbb5-df5a-58e2-98c5-fa72e5f277b4",
        "89b6526a-b995-5ca1-8387-5d135e3a20de",
    ],
    "inventory": [
        "0770f22a-466f-5688-b5c8-d1689e464462",
        "d6a2df67-795d-58f9-936f-5c5d8cc022a5",
        "804046c1-67a2-5528-b7b5-7dfed91c0239",
    ],
    "files": [
        "62706e71-bc6e-5e78-8ec5-4d3c8ca279bf",
        "8cbb73be-0fa9-5e83-a98e-df154c1fbc1c",
        "961408b0-27d2-552f-ad5f-26c33d4b75b7",
    ],
}

# ── 3. Verbatim quotes ────────────────────────────────────────────────────────
def q(text, customer_name, org, record_id):
    return {"text": text, "customer_name": customer_name, "org": org,
            "url": BASE_URL + record_id}

QUOTES = {
    "dashboards": {
        "complaints": [
            q("I couldn't figure out which category this would fall. I'm working on setting up a new control issue view. We used the Control Issues Overview (Global) as the base but changed the tables and fields to what we need. There are a somethings I can't figure out (and cannot find any help guides that relate to the new dashboards, everything is ABI which I'm not using).",
              "Laura", "Edgewell", "4d54abf5-d3d6-5634-8376-4e0d9a654559"),
            q("I will tell you trying to search things on the help center is difficult. Yeah. And you're looking for like, okay, how do I do this? And it's like go watch this 30 minute training? Yeah. And then it doesn't even answer my question.",
              "Stephanie De Silva", "Western Digital Technologies", "ea04f220-fb38-53d4-b884-45cc0bb225dc"),
            q("But we can see we have different dashboard for the controls assessments, risk, not a single one because leadership wants a single one single view.",
              "Pankul Bindal", "Clarivate Analytics LLC", "c2037c3d-20d2-5351-89cb-c3a584bb17c5"),
        ],
        "improvements": [
            q("I think having, yeah, I like having the structure in place and then just being able to toggle on the plan year. So I can just carry it forward into future years. So I prefer that way, but, yeah, OK.",
              "Joseph Gable", "Westinghouse Electric Company", "82df792c-0144-55a3-82c4-d04d0595d019"),
            q("I think we had a good conversation yesterday with Eliza about things that automatically overlap between some of these platforms. So things like disaster recovery, business continuity is a good example. There's another one that escapes data classification is another good example where there are controls that just inherently overlap across these frameworks and being able to see them on one board.",
              "Nathaniel Cartagena", "Eliquent Life Sciences, Inc.", "946a139b-cecc-5b9b-91b4-652991e00f61"),
        ],
        "praise": [
            q("Paige, are these dashboards customizable? Is it something we can tell you? We want it to look like or is it more of a template out of the box?",
              "Steph Copley", "TMG Insurance Services, LLC", "835e6dfc-fec0-590b-9bcb-c0d7acfaef80"),
            q("I mean, I think how it's operating is how I envisioned it and how I was hoping for it.",
              "Rachel Schlegel", "Family Dollar Inc", "f7935478-02f8-54e4-8fee-a2d909ff8eb3"),
        ],
    },
    "risks": {
        "complaints": [
            q("Hi team, We have created a risk assessment for all-risk, but the inherent and residual risk values are not appearing on the risk page. Could you please help identify the reason for this unexpected behaviour and provide a resolution? Thank you.",
              "Customer", "gds.ey.com", "c354a425-4586-58fa-a439-d3b5bf0ee7ea"),
            q("Yeah. I mean, I know you're doing your job but like we're just not using it because mostly it doesn't fit our culture. So we're a little bit more entrepreneurial informal, in terms of just how we are as an organization and so like trying to go and put specific risks and map it.",
              "Jeff Sebree", "Eagle Materials, Inc.", "9d24e3b3-44a5-57d2-9042-d804f5b267b9"),
            q("Did you talk about fixing in the full audit proposed? The reference in that cell there, that column, if you change the full audit proposed, if you change this to, yes. And… the next column over it references, no, that needs to be fixed, right?",
              "Thomas Jandernoa", "Jackson National Life Insurance Company", "6fb46561-cfaa-582c-928e-d94bad455fd5"),
        ],
        "improvements": [
            q("The difference to me is the data core that right now, if I look at all the stuff that's… the difference and that's actually a pretty large difference because we don't have the data core, right? So there are manual activities that need to happen in order for us to connect erm and audit and sox, and all that we can't do today in any way that is sustainable.",
              "Mahnkej2", "Harley Davidson", "ec328cb0-ae1b-5e4c-9fc8-8645065c86d6"),
            q("We wanted to go with it quickly, of course. But a lot of the things we do is in excel and outlook and things like that. So obviously the GRC tool will help us with that.",
              "Rick van dijk", "Arag Legal Insurance", "e7521e28-94dd-5bab-b76c-44cbf4caba0f"),
        ],
        "praise": [
            q("We have three, okay, three in the team. So that's it for risk. And I think maybe 50 people who would respond, I think got it.",
              "Rick van dijk", "Arag Legal Insurance", "e7521e28-94dd-5bab-b76c-44cbf4caba0f"),
        ],
    },
    "issues": {
        "complaints": [
            q("We are in process of creating a new Issue type, but we can't find how to customize its form template. We are starting in our Sandbox environment before we do the same in production. Abbi was not very helpful for this. Could you please show me where to go to change the layout for this new issue type?",
              "Customer", "huntington.com", "83d96394-c9b6-5ba5-8ff5-c0e344f03e82"),
            q("As part of our new issue creation process, we have a custom field we added called 'Type' which we've added custom risk category types to select from. We have two issues that are exist in our issues register that are tagged as Wiz Product type. I'd like recategorize these to the Operational risk category. However, I can't change the 'Type' for issues that already exist in Optro.",
              "Danna Lopez", None, "ecbbcd62-abd4-54fd-ad5b-fb5bff57b20d"),
            q("I want to add the FY field as a required field for all our Issue types. When I go to add a required field, FY does not show up in the list of options.",
              "Kristi Knutson", "hoaic.com", "a71698cd-0fb9-5775-a55d-5df999e31c2a"),
        ],
        "improvements": [
            q("I think a reporting structure would be good because then you have both options where if you needed to export it and provide them the data, great, you could do that. But then you also have the functionality of the report.",
              "Michelle Holland", "Cogent Bank", "2215c22a-f7d5-5ea2-a803-d2db0e4fa663"),
            q("I just discovered that one of our Approvers who has the Role, Stakeholder, is not able to view: Compensating Controls Impacted Policies (the field is there, but the policy name is not showing; however the policy is populated in the Exception Request) Impacted Risks",
              "Tiffany Beaver", "Kontoor Brands, Inc.", "2eb2271e-b014-57de-8faa-81ac15e1ed30"),
        ],
        "praise": [
            q("And again for that, I'll just continue to track, that feature request but just took some notes there on how you're kind of adjusting that plan for operational audits this year. Yeah.",
              "Philip Riesch", "Five Below, Inc.", "cdb07b22-0c4f-5241-a601-f1c17c843632"),
            q("Yeah. So for the issue side we are, we're working internally and it's in the wrap up phases here, but we've had to undertake kind of a huge overhaul of reviewing our issues, criteria, aligning our issues criteria with other lines of business, internal audit.",
              "Kristin Pace", "Glacier Bancorp, Inc.", "a4d43249-81e8-512f-a35f-e2485b96594d"),
        ],
    },
    "opsaudit": {
        "complaints": [
            q("We have been struggling to customize our field layout in one of our test sections. We only want to make updates to Test 0: Walkthrough — however, when I navigate to 'Customize Field Layout (Test 0: Walkthrough)' within 'More Actions' on a control page, the updates to the layout seem to get applied to all of our test sections.",
              "Customer", "ascendlearning.com", "9544ae88-d76e-59fa-82a4-e7ee139daab9"),
            q("Yeah, this looks more UI friendly. I feel user interface friendly. The one you're currently showing me and, yeah, status I'm just comparing. Give me a minute. I missed. We'll get… this looks good. More user friendly is what I get at.",
              "Kalyan Sastry Chaturvedula", "Wabtec", "452a7b5e-862d-508f-b584-7924be2b1a80"),
        ],
        "improvements": [
            q("During our planning and fieldwork process, there's a lot of manual processes that we go through as far as… Our notes, keeping track of the documentation that's received in the file. So we find that stuff takes a long time and we're going through different iterations. Probably version control is a concern occasionally because we're working out of spreadsheets.",
              "Melissa Saxon", "RFA Bank", "bebe910d-b05b-5c1a-ba25-b4bca6e72239"),
            q("I would say the ones I'm thinking of mocking are definitely repeatable and would be in the plan going forward with an idea of expanding the scope, right? So like I'll shout out an example, there's a revenue point percent of completion audits. We're trying to do for non stocks entities.",
              "Joey", "MasTec North America, Inc.", "957c3999-c3fb-537a-8d24-c2222130f622"),
        ],
        "praise": [
            q("And again for that, I'll just continue to track, that feature request but just took some notes there on how you're kind of adjusting that plan for operational audits this year. Yeah.",
              "Philip Riesch", "Five Below, Inc.", "cdb07b22-0c4f-5241-a601-f1c17c843632"),
            q("I think this is exactly how AI would empower audit to be real time and continuous monitoring of like 100 percent data sets to the full population. I think our SVP would be very excited for this one.",
              "Danyao Su", "Hyatt Corporation", "26f22fe3-b761-53f6-a1d7-cace26522c65"),
        ],
    },
    "workstream": {
        "complaints": [
            q("That permission is already set to 'Allow' but the user cannot see the survey templates or create a new one. It's my understanding that WorkStream Project: Can Create enables the user to create a workstream project --- not a template. Are you sure this information is correct??",
              "Renee", "tcenergy.com", "2196680e-1a2d-5c55-a06c-d01da7a8fe39"),
            q("Hi! We are experiencing a bug that, when an issue is closed, the WorkStream tasks no longer appear referenced in the action plan view. In addition, the Files section is moved to the bottom of the action plan view.",
              "Ismael Castro", "Evertec Group LLC", "ca0c5609-1afa-50b7-8af0-0ff05b3afb03"),
            q("Only do it at one time and then it closes where it's not like open for them to drop files in like over a period of time. Like they only have like one window to do that. So they'll wait until three, four weeks later, and then they'll submit everything. And then once they submit it, they can't do it again.",
              "Viraj Trivedi", "York Catholic District School Board", "81567270-d839-522a-99f3-8ff6c3f2fffb"),
        ],
        "improvements": [
            q("Hi, I'd like to schedule a call to discuss how to create workstream email reminders within workstream projects. Currently, when I go to a project template, I can't add any reminders and can't add schedule to any. My goal is to create a workstream project that sends automated emails on the first of every month.",
              "Customer", "ey.com", "0e67ea49-65fc-50eb-b0fb-14701dfc7d02"),
        ],
        "praise": [
            q("So this would go to management. So we'd be asking them to give us versus us pulling it. This is Hannah one question I have. Does it also do any comparisons to files provided in prior periods or is it only looking at columns and empties and periods?",
              "Hannah", "Tractor Supply", "9d89cf3e-e01f-5f5a-973a-f6956741b838"),
            q("We just use it for requesting evidence. So, I think, you know, it's been good so far.",
              "Courtney Tran", "Open Text Corporation", "8786829d-d9a5-5b2f-a5c3-95ff19a3f714"),
        ],
    },
    "settings": {
        "complaints": [
            q("I am in the Risk > Environment > Key Risk Indicators module but there is no New KRI button for me. I tried opening it in 3 different browsers, but the results are the same.",
              "Spencer Carroll", "yakimachief.com", "7f7583b3-a7c8-5a00-b89b-d6f777a60cf7"),
            q("Our users are no longer able to update their Action Plans that are assigned to them. This is causing a significant problem since I, as an Application Administrator, am the only one who can update them. I should not be editing these records since the audit trail will show that I updated them.",
              "Customer", "earlywaring.com", "82790820-41c9-55f1-aa30-3bd109c21e06"),
            q("Unwanted changes that pop up like surprise upgrades slow us down with additional clicks, tabs that are waste of time. Access rights is a mess; system so complex it is difficult to impossible to figure out what needs to be updated.",
              "Customer", "Crane NXT", "57ab85ba-425b-5f4a-b5a3-00e0360dd58a"),
        ],
        "improvements": [
            q("No, something changed that removed their access. I need your team to investigate why the access was removed.",
              "Customer", "earlywaring.com", "82790820-41c9-55f1-aa30-3bd109c21e06"),
        ],
        "praise": [],
    },
    "esg": {
        "complaints": [
            q("Just want to clarify - you're saying if the bulk update isn't working/isn't an option (it isn't working in quantitative metrics > Locations & assignments) the only option is to manually update all 658 metrics?",
              "Andrew Bilodeau", "MAA", "163c2915-70c9-5d6e-9a4a-18edc59cab64"),
            q("We got this extra resource and we found that was extremely valuable. We had time to focus so much more on, you know, good things. Now, she left us and, we cannot deal with all the workload that has come with the CSRD, new reporting to the group management team.",
              "Martina Persson Hollsten", "Boliden AB", "ead121af-e0f3-5fa5-b79f-229a67b9a642"),
        ],
        "improvements": [
            q("She is currently assessing our requirements when it comes to ESG specifically with regard to CSRD compliance, and overall like the double materiality and the supply chain assessment. Like those are the big pieces she's working on right now.",
              "Tara Mavrovitis", "Collibra", "9a25dcda-50da-5abb-baa9-da19c2647c05"),
            q("So just wanted to set up this meeting to get a better sense of, you know, guidewire what their expectations for ESG, anything that I should know as part of the sales handover?",
              "Reeti Patel", "SEG Holding, LLC", "efdba527-5f7e-5d9c-8bf2-fdfbd8c705e5"),
        ],
        "praise": [],
    },
    "tprm": {
        "complaints": [
            q("So we're forming that cohesive group to look at, use one system that we're looking at the same thing for all suppliers.",
              "Nick Spignazzi", "Albemarle Corporation", "44d2f5f5-1fde-5b43-a28e-48a14e9a0a1b"),
            q("We have our first due date tomorrow for the first round of sample data and questionnaires, cross comply. The reason we're not using that as heavily is because I've been one person for four and a half years, so we onboarded, we had planned to start using it for the audit and that just never came to fruition because I didn't have time.",
              "Jordan Roberts", "Alegeus Technologies LLC", "4f215f5d-a408-59ee-b663-49e4c8fac038"),
        ],
        "improvements": [
            q("I mean, as whatever direction if this hadn't happened, you know, we would have as we matured had been looking for tools to make it easier, right? As Tarek said, we're a small staff. So we have to respond with escalated technology rather than just pure manpower.",
              "Tom Bradbeer", "Xponential Fitness", "4fb5086e-97c3-564a-8ecb-9be636fa7199"),
            q("So I am in the cybersecurity team at the moment. I am sort of focusing on doing due diligence, cybersecurity, due diligence for our existing and new onboarding suppliers at the moment as we discussed that's all very manual. So we're looking for something to help us out with that.",
              "Kelli Barkes", "THE C & C GROUP LIMITED", "7245adeb-5af4-5ab9-8827-e4b1a3e3e11d"),
        ],
        "praise": [],
    },
    "narratives": {
        "complaints": [
            q("Hi, Previously, when working in AuditBoard, I could open a flowchart and choose 'Edit in Lucidchart'. After making updates in Lucid, I would select 'Post to App', return to the AuditBoard flowchart, and click 'Refresh Lucidchart Image', and my changes would sync correctly. Right now, none of my edits are updating across multiple flowcharts. The 'Post to App → Refresh Lucidchart Image' workflow no longer pushes changes back into AuditBoard.",
              "Tyler Tweit", "sleepnumber.com", "cae644ff-dbe8-54ee-9ef1-7b4b279cd6a2"),
            q("In the narrative 'Main - Financial Statement', the most recent few versions are corrupt. When I try to open it, I get the error 'Sorry, Word ran into a problem opening this document in a browser. To view this document please open it in the desktop version of Microsoft Word'. I need the most recent working version restored.",
              "Sarah Watson", "rti.org", "803e207a-35a0-5951-9b98-00042adf29d4"),
        ],
        "improvements": [
            q("If you have a visio flowchart, can you modify it, or you cannot modify? Because currently, my biggest problem is I cannot modify my flowchart. If I need any change, I always have to like email RSM and ask them to do the changes.",
              "Sarka Lostakova", "Neurona Therapeutics, Inc.", "96cd7f67-32cf-58c9-8753-a94fc59915c8"),
            q("I don't know how we can build it within the auditboard. Frankly speaking. So we built it separately and we just have PDF files in auditboard with narratives, which is not very helpful because if we have an update or change, then it's not going to be automatically updated.",
              "Victoria Ignatenko", "Wealthsimple", "b36d21ef-7e14-5642-ae65-e0cef715be13"),
        ],
        "praise": [],
    },
    "regcomply": {
        "complaints": [
            q("Yeah, we're managing this in spreadsheets. So there are two spreadsheets. One is maintained by the policy team. They are the ones who are tracking the laws that are being introduced and doing the horizon scanning. And the second spreadsheet we have is what we're calling the reg readiness, single source of truth which is for every law that we have to comply.",
              "Nandita", "DoorDash", "a241d85a-d420-5f51-80b2-8ec9ef9dbbf1"),
            q("The reason why we wanted to even get a vendor is we want to make sure we're capturing everything. We have plans in different states. So again, we're not just looking at federal. We're looking at state and from state to state. It could vary. So, this is one of the biggest reason why we wanted that push to kind of get something a vendor versus having one person go out and look.",
              "Tracey Letang", "Softheon, Inc.", "637e16d1-75dc-5d2e-bb31-814475660f7e"),
        ],
        "improvements": [
            q("156 last time I counted, yeah.",
              "J. Mey", "Nedbank Group", "5ddd2899-4239-5abd-9255-6abe6972ce4b"),
        ],
        "praise": [],
    },
    "exceptions": {
        "complaints": [
            q("We have two different exception process. We are in policy, and then we have the policy exceptions or we can create a policy exception here. When you click that it is an issue, not an exception… it's like an issue, really the standalone issue that are the issues we have, not the exceptions, policy exception.",
              "Pankul Bindal", "Clarivate Analytics LLC", "c2037c3d-20d2-5351-89cb-c3a584bb17c5"),
            q("Post service it would be great to be able to see the tickets we raise and status on a dashboard and use this to follow up on items.",
              "Customer", "Nedbank Group", "80ecaa2b-b32b-591c-bdc2-737d4aad511f"),
        ],
        "improvements": [],
        "praise": [],
    },
    "integrations": {
        "complaints": [
            q("After IT changed the info back, I was able to log in SSO. So I think I'm ok. If you'll let me know once you've put my account back to SAML, I'll try in an incognito window to make sure?",
              "Tracy Graham", "Caterpillar", "92de9875-7783-5e94-905c-0a05a7ad4b53"),
            q("All of our users require single sign on unless it's a valid reason for them to not have that. And that ensures that when someone leaves the company, their access gets removed from the system. With this, her access wouldn't have gotten removed. So support essentially changed the access without asking us.",
              "Aksa Ahmed", "Carrier Corporation", "28fdc99f-5ee8-5e08-b17d-4b898d0821b9"),
        ],
        "improvements": [
            q("We're seeing just from some of our clients more in the IT risk side, they would like to see more of if in their existing platform, if Optro can integrate with, you know, specific applications. I know you had recently announced about Okta and Workday and some of the other applications, but our clients are looking for how to continuously monitor for change management.",
              "Kathleen Huang", "CrossCountry Consulting", "d348ba1e-1c73-5d79-b71f-de29365a6d85"),
        ],
        "praise": [],
    },
    "automations": {
        "complaints": [
            q("Need help deleting the users in the attached email. Given that the AuditBoard API is shared between the SCIM and other endpoints with the same overall rate limit, there is impact to other automations that rely on this API for SOX control management. The rate limit is being continuously exceeded by the SCIM process right now and not leaving enough bandwidth for other requests.",
              "Alejandra", "Intel", "c491114e-f5e0-5f80-9acc-c91a470a3bc4"),
            q("Hello, I've searched and asked the chatbot about CSA workflows. We're wondering how Control Owners/Question Owners are notified of the result (effectiveness once status is 'reviewed') of their control self-assessments they submit.",
              "Customer", "sofi.org", "0ed4dea1-48b7-5cd0-926f-f101099d999e"),
        ],
        "improvements": [],
        "praise": [
            q("I think this is exactly how AI would empower audit to be real time and continuous monitoring of like 100 percent data sets to the full population. I think our SVP would be very excited for this one.",
              "Danyao Su", "Hyatt Corporation", "26f22fe3-b761-53f6-a1d7-cace26522c65"),
        ],
    },
    "inventory": {
        "complaints": [
            q("Do Zach? Yeah, no, it's a good call out. I was going to say it's actually the former of your statement — the hierarchy is driven by the type field, Zach, but you're right. Every time you create an auditable entity, you are associating an inventory type to it. So, yes, like everything will be driven by the type that every audit and auditable entity record is connected to.",
              "Victor Vazquez (Agent)", None, "96826421-7c20-599c-a547-d4a3349a88fb"),
            q("I think the experience that I remember was that we do have three, I guess three independent risk assessments that are performed. And the way that audit board is structured is more like one unified risk assessment.",
              "Reuben Philipose", "Henry Schein", "191d40a4-9730-5c79-9d4e-07fc96f38cf"),
        ],
        "improvements": [],
        "praise": [],
    },
    "ai-governance": {
        "complaints": [],
        "improvements": [],
        "praise": [
            q("So the way I'm thinking about it is I imagine guys, the way I think the future of AI gov is going to be, is there's going to be a technology layer of governance. And then there's going to be a human kind of overseeing over the loop, so to speak. And the technology layer is going to help do two things. There's going to be an orchestration layer that orchestrates your governance program across all the different complexities.",
              "Guru Sethupathy (Agent)", None, "746ffe46-d89d-5250-84c4-c05ceec6857a"),
            q("Shadow AI is a big problem. Okay. Yeah, a lot of organizations, it's probably one of their bigger problems not only from an internal perspective with regards to internally developed or used applications, but also from a third party perspective where a vendor that they already have onboarded an application or piece of technology, then implements some kind of AI related module or functionality.",
              "Jim Packer", "GuidePoint Security LLC", "746ffe46-d89d-5250-84c4-c05ceec6857a"),
        ],
    },
    "files": {
        "complaints": [
            q("Better save functionality — prompting the user to save before closing (or autosaving upon document close). Auto check-in working papers when you logout of AB. Comment filter to show only open comments and also a comment status/priority so we can mark some comments as critical. See more of the work paper name in the workstep.",
              "Customer", "Michigan Office of the Auditor", "8cbb73be-0fa9-5e83-a98e-df154c1fbc1c"),
            q("Recurring issues when uploading documents to the system (stuck at 100% not uploading).",
              "Customer", "Walmart Inc.", "961408b0-27d2-552f-ad5f-26c33d4b75b7"),
        ],
        "improvements": [],
        "praise": [],
    },
    "timesheets": {
        "complaints": [],
        "improvements": [],
        "praise": [],
    },
    "asq": {
        "complaints": [
            q("Two forms. Typically, it's either going to be a set of documents like excel spreadsheets that we have to fill out. And then sometimes it's through like Panerais, which is a web based questionnaire system.",
              "Bruce Talbot", "Okland Construction", "a95e25e4-4192-539c-b60a-ae5847959a21"),
        ],
        "improvements": [],
        "praise": [],
    },
    "itrm": {
        "complaints": [
            q("ITRM Mitigation Plans and ITRM Risk Insights are not pulling data from our risk register. These should be out of the box features that are not connecting to the data.",
              "Chip White", None, "f1b08241-1446-55b3-8554-cb7cb9320f12"),
        ],
        "improvements": [
            q("I got our IT application listing. I imported that here into assets and inventory. So we have 53 right now. And then I started adding them here under entities. I added 30. And then I kind of stopped myself just to make sure I was doing this, right?",
              "Jamie Natale", "Municipal Credit Union", "0b84e9fb-9ed7-56cd-90b7-3b262be4c8c3"),
        ],
        "praise": [],
    },
}


# ── Apply updates ────────────────────────────────────────────────────────────

with open("enterpret-modules.json") as f:
    data = json.load(f)

for module in data:
    mid = module["module"]["id"]

    # ── A. Move rank > 15 themes into deep_dive.subthemes ──────────────────
    complaints = module.get("top_complaints") or {}
    themes = complaints.get("themes") or []
    main_themes = [t for t in themes if t["rank"] <= 15]
    sub_themes  = [t for t in themes if t["rank"] > 15]
    if sub_themes:
        complaints["themes"] = main_themes
        deep = complaints.get("deep_dive") or {}
        deep["subthemes"] = [{"theme": t["theme"], "count": t["count"]} for t in sub_themes]
        complaints["deep_dive"] = deep

    # ── B. Priority recommendation short titles ─────────────────────────────
    if mid in PRIORITY_TITLES:
        titles = PRIORITY_TITLES[mid]
        recs = module.get("priority_recommendations") or []
        for rec in recs:
            idx = rec["rank"] - 1
            if 0 <= idx < len(titles):
                rec["short_title"] = titles[idx]

    # ── C. NPS detractor URLs ───────────────────────────────────────────────
    if mid in NPS_URLS:
        urls = NPS_URLS[mid]
        nps_comments = module.get("nps_detractor_comments") or []
        for i, comment in enumerate(nps_comments):
            if i < len(urls):
                comment["url"] = BASE_URL + urls[i]

    # ── D. Verbatim quotes ──────────────────────────────────────────────────
    if mid in QUOTES:
        q_data = QUOTES[mid]
        if "complaints" in q_data:
            (module.get("top_complaints") or {})["quotes"] = q_data["complaints"]
        if "improvements" in q_data:
            (module.get("top_improvements") or {})["quotes"] = q_data["improvements"]
        if "praise" in q_data:
            (module.get("praise") or {})["quotes"] = q_data["praise"]


with open("enterpret-modules.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done. Summary of changes:")
for module in data:
    mid = module["module"]["id"]
    complaints = module.get("top_complaints") or {}
    sub = len((complaints.get("deep_dive") or {}).get("subthemes") or [])
    cq  = len(complaints.get("quotes") or [])
    iq  = len((module.get("top_improvements") or {}).get("quotes") or [])
    pq  = len((module.get("praise") or {}).get("quotes") or [])
    nps = module.get("nps_detractor_comments") or []
    nu  = sum(1 for c in nps if "url" in c)
    nt  = sum(1 for r in (module.get("priority_recommendations") or []) if "short_title" in r)
    print(f"  {mid}: subthemes={sub}, cq={cq}, iq={iq}, pq={pq}, nps_urls={nu}/{len(nps)}, titles={nt}")
