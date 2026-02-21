# PowerPoint Presentation Examples

## Example 1: Creating a Business Presentation

```javascript
// Step 1: Activate required tools
activate_presentation_creation_and_management();
activate_text_placeholder_management();
activate_content_management_tools();

// Step 2: Create presentation
mcp_ppt_create_presentation({
  filename: "q3_business_review.pptx",
  title: "Q3 2025 Business Review"
});

// Step 3: Create title slide
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 0,
  text: "Q3 2025 Business Review"
});
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 1,
  text: "Finance Division · October 2025"
});

// Step 4: Add agenda slide
mcp_ppt_add_slide({ filename: "q3_business_review.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({
  slide_index: 1,
  placeholder_index: 0,
  text: "Agenda"
});
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 1,
  placeholder_index: 1,
  bullet_points: [
    "Financial Performance Overview",
    "Key Metrics and KPIs",
    "Regional Analysis",
    "Strategic Initiatives",
    "Q4 Outlook"
  ]
});

// Step 5: Add content slide with metrics
mcp_ppt_add_slide({ filename: "q3_business_review.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({
  slide_index: 2,
  placeholder_index: 0,
  text: "Key Financial Metrics"
});
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 2,
  placeholder_index: 1,
  bullet_points: [
    "Revenue: $1.8M (+20% YoY)",
    "Gross Margin: 45% (+3pp)",
    "Operating Income: $540K",
    "Net Income: $405K",
    "EPS: $0.45"
  ]
});

// Step 6: Save presentation
mcp_ppt_save_presentation({ filename: "q3_business_review.pptx" });
```

## Example 2: Creating a Data-Heavy Presentation with Charts

```javascript
// Create presentation with multiple chart slides
activate_presentation_creation_and_management();
activate_text_placeholder_management();
activate_content_management_tools();

mcp_ppt_create_presentation({
  filename: "data_analysis.pptx",
  title: "Q3 Data Analysis"
});

// Title slide
mcp_ppt_populate_placeholder({ slide_index: 0, placeholder_index: 0, text: "Q3 Data Analysis" });
mcp_ppt_populate_placeholder({ slide_index: 0, placeholder_index: 1, text: "Analytics Team" });

// Revenue chart slide
mcp_ppt_add_slide({ filename: "data_analysis.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 1, placeholder_index: 0, text: "Revenue Trends" });
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 1,
  placeholder_index: 1,
  bullet_points: [
    "Strong growth in APAC region",
    "Americas showing steady improvement",
    "EMEA exceeding targets"
  ]
});
mcp_ppt_manage_image({
  slide_index: 1,
  operation: "add",
  image_path: "./charts/revenue_by_region.png",
  left: 1.0,
  top: 2.5,
  width: 8.0,
  height: 4.0
});
mcp_ppt_manage_text({
  slide_index: 1,
  operation: "add",
  text: "Source: Internal BI System",
  font_size: 9,
  italic: true,
  left: 7.0,
  top: 6.8,
  width: 2.0,
  height: 0.3,
  alignment: "right"
});

// Customer acquisition chart slide
mcp_ppt_add_slide({ filename: "data_analysis.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 2, placeholder_index: 0, text: "Customer Acquisition" });
mcp_ppt_manage_image({
  slide_index: 2,
  operation: "add",
  image_path: "./charts/customer_funnel.png",
  left: 1.0,
  top: 1.5,
  width: 8.0,
  height: 4.5
});

mcp_ppt_save_presentation({ filename: "data_analysis.pptx" });
```

## Example 3: Template-Based Presentation with Branding

```javascript
// Create presentation from template
activate_presentation_creation_and_management();
activate_text_placeholder_management();
activate_template_application_tools();
activate_content_management_tools();

// Create from template
mcp_ppt_create_presentation({
  filename: "monthly_update.pptx",
  title: "Monthly Status Update"
});

// Apply brand template
mcp_ppt_apply_template({
  filename: "monthly_update.pptx",
  template_name: "BrandTemplate.pptx",
  apply_to_all: true
});

// Title slide
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 0,
  text: "November 2025 Status Update"
});
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 1,
  text: "Engineering Department"
});

// Progress slide
mcp_ppt_add_slide({ filename: "monthly_update.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 1, placeholder_index: 0, text: "Project Progress" });
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 1,
  placeholder_index: 1,
  bullet_points: [
    "Platform Migration: 85% complete",
    "API Gateway: Deployed to production",
    "Dashboard Redesign: In QA",
    "Mobile App Beta: Launched"
  ]
});

// Blockers slide
mcp_ppt_add_slide({ filename: "monthly_update.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 2, placeholder_index: 0, text: "Key Blockers" });
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 2,
  placeholder_index: 1,
  bullet_points: [
    "Database migration pending security review",
    "API rate limiting needs performance testing",
    "Third-party authentication provider delay"
  ]
});

// Next steps slide
mcp_ppt_add_slide({ filename: "monthly_update.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 3, placeholder_index: 0, text: "Next Steps" });
mcp_ppt_add_bullet_points_to_placeholder({
  slide_index: 3,
  placeholder_index: 1,
  bullet_points: [
    "Complete platform migration by Nov 15",
    "Performance testing on API Gateway",
    "Finalize dashboard UI components",
    "Prepare mobile app public beta"
  ]
});

mcp_ppt_save_presentation({ filename: "monthly_update.pptx" });
```

## Example 4: Presentation with Mixed Formatting

```javascript
// Create presentation with mixed text formatting
activate_presentation_creation_and_management();
activate_text_placeholder_management();

mcp_ppt_create_presentation({
  filename: "kpi_dashboard.pptx",
  title: "KPI Dashboard"
});

// Title slide with styled subtitle
mcp_ppt_populate_placeholder({
  slide_index: 0,
  placeholder_index: 0,
  text: "Q3 KPI Performance"
});

// Add free text box with mixed formatting
mcp_ppt_manage_text({
  slide_index: 0,
  operation: "add",
  text_runs: [
    { text: "Prepared by: ", bold: false, font_size: 14 },
    { text: "Finance Team", bold: true, font_size: 14, color: [31, 78, 120] }
  ],
  left: 2.0,
  top: 4.0,
  width: 6.0,
  height: 0.5,
  alignment: "center"
});

// KPI highlights slide
mcp_ppt_add_slide({ filename: "kpi_dashboard.pptx", layout_index: 2 });
mcp_ppt_populate_placeholder({ slide_index: 1, placeholder_index: 0, text: "KPI Highlights" });

// Add KPI callouts with mixed formatting
mcp_ppt_manage_text({
  slide_index: 1,
  operation: "add",
  text_runs: [
    { text: "Revenue: ", bold: true, font_size: 18, color: [31, 78, 120] },
    { text: "$1.8M ", bold: true, font_size: 18 },
    { text: "(", font_size: 18 },
    { text: "+20%", bold: true, font_size: 18, color: [0, 128, 0] },
    { text: ")", font_size: 18 }
  ],
  left: 1.0,
  top: 2.0,
  width: 3.0,
  height: 0.5
});

mcp_ppt_manage_text({
  slide_index: 1,
  operation: "add",
  text_runs: [
    { text: "Margin: ", bold: true, font_size: 18, color: [31, 78, 120] },
    { text: "45% ", bold: true, font_size: 18 },
    { text: "(", font_size: 18 },
    { text: "+3pp", bold: true, font_size: 18, color: [0, 128, 0] },
    { text: ")", font_size: 18 }
  ],
  left: 1.0,
  top: 2.8,
  width: 3.0,
  height: 0.5
});

mcp_ppt_save_presentation({ filename: "kpi_dashboard.pptx" });
```
