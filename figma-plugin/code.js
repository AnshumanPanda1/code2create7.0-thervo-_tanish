// THERVO - ACM Figma Plugin Generator Script
// Single Source of Truth: AI-Driven_Sensor-Free_Predictive_Cooling_LIVE.html
// Generates 100% native, fully editable Figma layers, design tokens, master components, and prototype links.

async function generateTherVOApp() {
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  await figma.loadFontAsync({ family: "Inter", style: "Medium" });
  await figma.loadFontAsync({ family: "Inter", style: "SemiBold" });
  await figma.loadFontAsync({ family: "Inter", style: "Bold" });
  await figma.loadFontAsync({ family: "Roboto", style: "Regular" });
  await figma.loadFontAsync({ family: "Roboto", style: "Medium" });
  await figma.loadFontAsync({ family: "Roboto", style: "Bold" });

  // 1. CREATE PAGE
  const page = figma.createPage();
  page.name = "THERVO - ACM (Demo Figma)";
  figma.currentPage = page;

  // 2. DESIGN TOKENS (LIGHT THEME MATCHING HTML)
  const colors = {
    bgApp: { r: 0.972, g: 0.98, b: 0.988 },         // #f8fafc
    bgSurface: { r: 1.0, g: 1.0, b: 1.0 },           // #ffffff
    bgSubtle: { r: 0.945, g: 0.96, b: 0.976 },       // #f1f5f9
    bgMuted: { r: 0.886, g: 0.91, b: 0.941 },        // #e2e8f0
    borderLight: { r: 0.886, g: 0.91, b: 0.941 },    // #e2e8f0
    borderColor: { r: 0.796, g: 0.835, b: 0.882 },   // #cbd5e1
    
    textPrimary: { r: 0.059, g: 0.09, b: 0.165 },    // #0f172a
    textSecondary: { r: 0.278, g: 0.333, b: 0.412 },  // #475569
    textMuted: { r: 0.392, g: 0.455, b: 0.545 },     // #64748b
    textLight: { r: 0.58, g: 0.639, b: 0.722 },      // #94a3b8

    brandPrimary: { r: 0.118, g: 0.251, b: 0.686 },  // #1e40af (Navy Blue)
    brandHover: { r: 0.114, g: 0.306, b: 0.847 },    // #1d4ed8
    brandLight: { r: 0.937, g: 0.965, b: 1.0 },      // #eff6ff
    brandAccent: { r: 0.008, g: 0.518, b: 0.78 },     // #0284c7 (Cyan-Blue)

    riskLow: { r: 0.086, g: 0.639, b: 0.29 },        // #16a34a (Green)
    riskLowBg: { r: 0.863, g: 0.988, b: 0.906 },     // #dcfce7
    
    riskMed: { r: 0.851, g: 0.467, b: 0.024 },       // #d97706 (Amber)
    riskMedBg: { r: 0.996, g: 0.953, b: 0.78 },      // #fef3c7

    riskHigh: { r: 0.918, g: 0.345, b: 0.047 },      // #ea580c (Orange)
    riskHighBg: { r: 1.0, g: 0.929, b: 0.835 },      // #ffedd5

    riskCrit: { r: 0.863, g: 0.149, b: 0.149 },      // #dc2626 (Red)
    riskCritBg: { r: 0.996, g: 0.886, b: 0.886 }      // #fee2e2
  };

  function solid(color) {
    return [{ type: 'SOLID', color: color }];
  }

  // 3. MASTER COMPONENTS
  const navComponent = figma.createComponent();
  navComponent.name = "Navigation Link";
  navComponent.layoutMode = "HORIZONTAL";
  navComponent.paddingLeft = 14; navComponent.paddingRight = 14;
  navComponent.paddingTop = 6; navComponent.paddingBottom = 6;
  navComponent.cornerRadius = 6;
  navComponent.fills = [];
  const navText = figma.createText();
  navText.name = "Tab Title";
  navText.fontName = { family: "Inter", style: "Medium" };
  navText.fontSize = 13;
  navText.fills = solid(colors.textSecondary);
  navText.characters = "Overview";
  navComponent.appendChild(navText);

  const rackComponent = figma.createComponent();
  rackComponent.name = "Master Rack Unit";
  rackComponent.layoutMode = "VERTICAL";
  rackComponent.paddingLeft = 12; rackComponent.paddingRight = 12;
  rackComponent.paddingTop = 10; rackComponent.paddingBottom = 10;
  rackComponent.cornerRadius = 6;
  rackComponent.fills = solid(colors.bgSurface);
  rackComponent.strokes = solid(colors.borderLight);
  rackComponent.strokeWeight = 1;
  rackComponent.itemSpacing = 8;
  rackComponent.resize(240, 160);

  const rHeader = figma.createFrame();
  rHeader.layoutMode = "HORIZONTAL";
  rHeader.primaryAxisSizingMode = "FIXED";
  rHeader.counterAxisSizingMode = "AUTO";
  rHeader.layoutAlign = "STRETCH";
  rHeader.fills = [];
  const rTitle = figma.createText();
  rTitle.fontName = { family: "Inter", style: "Bold" };
  rTitle.fontSize = 13;
  rTitle.fills = solid(colors.textPrimary);
  rTitle.characters = "RACK-A11";
  rHeader.appendChild(rTitle);

  const rBadge = figma.createFrame();
  rBadge.layoutMode = "HORIZONTAL";
  rBadge.paddingLeft = 6; rBadge.paddingRight = 6;
  rBadge.paddingTop = 2; rBadge.paddingBottom = 2;
  rBadge.cornerRadius = 4;
  rBadge.fills = solid(colors.riskLowBg);
  const rBadgeText = figma.createText();
  rBadgeText.fontName = { family: "Inter", style: "Bold" };
  rBadgeText.fontSize = 10;
  rBadgeText.fills = solid(colors.riskLow);
  rBadgeText.characters = "25% LOW";
  rBadge.appendChild(rBadgeText);
  rHeader.appendChild(rBadge);
  rackComponent.appendChild(rHeader);

  // 4. VIEWS DEFINITION (7 VIEWS INCLUDING AI MODEL)
  const views = [
    { id: "overview", title: "1. Overview (Dashboard)" },
    { id: "thermal-map", title: "2. Thermal Map" },
    { id: "racks", title: "3. Racks" },
    { id: "predictions", title: "4. Predictions" },
    { id: "ai-model", title: "5. AI Model Pipeline" },
    { id: "events", title: "6. Events Audit Log" },
    { id: "datasets", title: "7. Datasets & Provenance" }
  ];

  const createdFrames = {};

  for (let i = 0; i < views.length; i++) {
    const view = views[i];
    const frame = figma.createFrame();
    frame.name = view.title;
    frame.resize(1920, 1080);
    frame.x = i * 2000;
    frame.y = 0;
    frame.fills = solid(colors.bgApp);
    frame.layoutMode = "VERTICAL";
    frame.itemSpacing = 0;

    // --- A. APP HEADER ---
    const header = figma.createFrame();
    header.name = "App Header";
    header.resize(1920, 60);
    header.layoutMode = "HORIZONTAL";
    header.primaryAxisAlignItems = "SPACE_BETWEEN";
    header.counterAxisAlignItems = "CENTER";
    header.paddingLeft = 24; header.paddingRight = 24;
    header.fills = solid(colors.bgSurface);
    header.strokes = solid(colors.borderLight);
    header.strokeWeight = 1;

    const brand = figma.createFrame();
    brand.layoutMode = "HORIZONTAL";
    brand.itemSpacing = 8;
    brand.counterAxisAlignItems = "CENTER";
    brand.fills = [];
    
    const logoIcon = figma.createRectangle();
    logoIcon.resize(20, 20);
    logoIcon.cornerRadius = 4;
    logoIcon.fills = solid(colors.brandPrimary);
    brand.appendChild(logoIcon);

    const title = figma.createText();
    title.fontName = { family: "Inter", style: "Bold" };
    title.fontSize = 18;
    title.fills = solid(colors.textPrimary);
    title.characters = "THERVO - ACM";
    brand.appendChild(title);
    header.appendChild(brand);

    // Nav Links
    const nav = figma.createFrame();
    nav.name = "App Navigation";
    nav.layoutMode = "HORIZONTAL";
    nav.itemSpacing = 6;
    nav.fills = [];

    const navTabs = [
      { name: "Overview", tab: "overview" },
      { name: "Thermal Map", tab: "thermal-map" },
      { name: "Racks", tab: "racks" },
      { name: "Predictions", tab: "predictions" },
      { name: "AI Model", tab: "ai-model" },
      { name: "Events", tab: "events" },
      { name: "Datasets", tab: "datasets" }
    ];

    navTabs.forEach(t => {
      const link = navComponent.createInstance();
      const txt = link.findOne(n => n.type === "TEXT");
      if (txt) txt.characters = t.name;
      if (t.tab === view.id) {
        link.fills = solid(colors.brandLight);
        if (txt) {
          txt.fills = solid(colors.brandAccent);
          txt.fontName = { family: "Inter", style: "SemiBold" };
        }
      }
      nav.appendChild(link);
    });
    header.appendChild(nav);

    // Controls
    const controls = figma.createFrame();
    controls.layoutMode = "HORIZONTAL";
    controls.itemSpacing = 16;
    controls.counterAxisAlignItems = "CENTER";
    controls.fills = [];

    const facSelect = figma.createFrame();
    facSelect.layoutMode = "HORIZONTAL";
    facSelect.paddingLeft = 10; facSelect.paddingRight = 10;
    facSelect.paddingTop = 5; facSelect.paddingBottom = 5;
    facSelect.cornerRadius = 6;
    facSelect.fills = solid(colors.bgSubtle);
    facSelect.strokes = solid(colors.borderLight);
    facSelect.strokeWeight = 1;
    const facText = figma.createText();
    facText.fontName = { family: "Inter", style: "Medium" };
    facText.fontSize = 12;
    facText.fills = solid(colors.textPrimary);
    facText.characters = "Main Facility ▾";
    facSelect.appendChild(facText);
    controls.appendChild(facSelect);

    const liveInd = figma.createFrame();
    liveInd.layoutMode = "HORIZONTAL";
    liveInd.itemSpacing = 6;
    liveInd.counterAxisAlignItems = "CENTER";
    liveInd.fills = [];
    const dot = figma.createEllipse();
    dot.resize(8, 8);
    dot.fills = solid(colors.riskLow);
    const liveText = figma.createText();
    liveText.fontName = { family: "Inter", style: "Medium" };
    liveText.fontSize = 12;
    liveText.fills = solid(colors.textPrimary);
    liveText.characters = "Live";
    liveInd.appendChild(dot);
    liveInd.appendChild(liveText);
    controls.appendChild(liveInd);

    const switchBadge = figma.createFrame();
    switchBadge.layoutMode = "HORIZONTAL";
    switchBadge.paddingLeft = 10; switchBadge.paddingRight = 10;
    switchBadge.paddingTop = 4; switchBadge.paddingBottom = 4;
    switchBadge.cornerRadius = 16;
    switchBadge.itemSpacing = 8;
    switchBadge.fills = solid(colors.bgSubtle);
    switchBadge.strokes = solid(colors.borderLight);
    switchBadge.strokeWeight = 1;
    const sLabel = figma.createText();
    sLabel.fontName = { family: "Inter", style: "Bold" };
    sLabel.fontSize = 11;
    sLabel.fills = solid(colors.brandPrimary);
    sLabel.characters = "THERVO";
    const sStatus = figma.createText();
    sStatus.fontName = { family: "Inter", style: "Bold" };
    sStatus.fontSize = 11;
    sStatus.fills = solid(colors.riskLow);
    sStatus.characters = "ON";
    switchBadge.appendChild(sLabel);
    switchBadge.appendChild(sStatus);
    controls.appendChild(switchBadge);

    const avatar = figma.createEllipse();
    avatar.resize(28, 28);
    avatar.fills = solid(colors.brandPrimary);
    controls.appendChild(avatar);

    header.appendChild(controls);
    frame.appendChild(header);

    // --- B. STATUS BAR STRIP ---
    const statusStrip = figma.createFrame();
    statusStrip.name = "Global Status Strip";
    statusStrip.resize(1920, 36);
    statusStrip.layoutMode = "HORIZONTAL";
    statusStrip.itemSpacing = 16;
    statusStrip.paddingLeft = 24; statusStrip.paddingRight = 24;
    statusStrip.counterAxisAlignItems = "CENTER";
    statusStrip.fills = solid(colors.bgSurface);
    statusStrip.strokes = solid(colors.borderLight);
    statusStrip.strokeWeight = 1;

    const stripItems = [
      { label: "SYSTEM STATUS", val: "Operational", color: colors.riskLow },
      { label: "THERMAL RISK", val: "0 racks require attention", color: colors.textPrimary },
      { label: "COOLING INTERVENTIONS", val: "0 active", color: colors.textPrimary },
      { label: "MODEL INFERENCE", val: "Live (GNN + XGB)", color: colors.brandPrimary },
      { label: "LAST UPDATE", val: "SIM TIME: 00:00", color: colors.textMuted }
    ];

    stripItems.forEach((si, idx) => {
      const itemFrame = figma.createFrame();
      itemFrame.layoutMode = "HORIZONTAL";
      itemFrame.itemSpacing = 6;
      itemFrame.fills = [];
      const lbl = figma.createText();
      lbl.fontName = { family: "Inter", style: "Bold" };
      lbl.fontSize = 10;
      lbl.fills = solid(colors.textMuted);
      lbl.characters = si.label;
      const val = figma.createText();
      val.fontName = { family: "Inter", style: "Bold" };
      val.fontSize = 11;
      val.fills = solid(si.color);
      val.characters = si.val;
      itemFrame.appendChild(lbl);
      itemFrame.appendChild(val);
      statusStrip.appendChild(itemFrame);

      if (idx < stripItems.length - 1) {
        const div = figma.createRectangle();
        div.resize(1, 16);
        div.fills = solid(colors.borderLight);
        statusStrip.appendChild(div);
      }
    });
    frame.appendChild(statusStrip);

    // --- C. MAIN CONTENT AREA ---
    const content = figma.createFrame();
    content.name = "Main Content Body";
    content.layoutMode = "VERTICAL";
    content.paddingLeft = 24; content.paddingRight = 24;
    content.paddingTop = 20; content.paddingBottom = 20;
    content.itemSpacing = 20;
    content.fills = [];
    content.resize(1920, 984);

    if (view.id === "overview") {
      const cardOverview = figma.createFrame();
      cardOverview.name = "Overview Dashboard";
      cardOverview.layoutMode = "VERTICAL";
      cardOverview.paddingLeft = 20; cardOverview.paddingRight = 20;
      cardOverview.paddingTop = 16; cardOverview.paddingBottom = 16;
      cardOverview.cornerRadius = 8;
      cardOverview.fills = solid(colors.bgSurface);
      cardOverview.strokes = solid(colors.borderLight);
      cardOverview.strokeWeight = 1;
      cardOverview.resize(1872, 750);
      content.appendChild(cardOverview);
    } else if (view.id === "ai-model") {
      const cardAi = figma.createFrame();
      cardAi.name = "AI Model Pipeline & Live Topology";
      cardAi.layoutMode = "VERTICAL";
      cardAi.paddingLeft = 20; cardAi.paddingRight = 20;
      cardAi.paddingTop = 16; cardAi.paddingBottom = 16;
      cardAi.cornerRadius = 8;
      cardAi.fills = solid(colors.bgSurface);
      cardAi.strokes = solid(colors.borderLight);
      cardAi.strokeWeight = 1;
      cardAi.resize(1872, 750);

      const aiTitle = figma.createText();
      aiTitle.fontName = { family: "Inter", style: "Bold" };
      aiTitle.fontSize = 18;
      aiTitle.fills = solid(colors.textPrimary);
      aiTitle.characters = "AI Model — Thermal Intelligence Engine Pipeline";
      cardAi.appendChild(aiTitle);
      content.appendChild(cardAi);
    } else {
      const viewCard = figma.createFrame();
      viewCard.name = `${view.title} Content`;
      viewCard.layoutMode = "VERTICAL";
      viewCard.paddingLeft = 24; viewCard.paddingRight = 24;
      viewCard.paddingTop = 24; viewCard.paddingBottom = 24;
      viewCard.cornerRadius = 8;
      viewCard.fills = solid(colors.bgSurface);
      viewCard.strokes = solid(colors.borderLight);
      viewCard.strokeWeight = 1;
      viewCard.resize(1872, 800);

      const vTitle = figma.createText();
      vTitle.fontName = { family: "Inter", style: "Bold" };
      vTitle.fontSize = 20;
      vTitle.fills = solid(colors.textPrimary);
      vTitle.characters = view.title;
      viewCard.appendChild(vTitle);
      content.appendChild(viewCard);
    }

    frame.appendChild(content);
    createdFrames[view.id] = frame;
  }

  // 5. PROTOTYPE CONNECTIONS
  for (let viewId in createdFrames) {
    const sourceFrame = createdFrames[viewId];
    const navContainer = sourceFrame.findOne(n => n.name === "App Navigation");
    if (navContainer) {
      const links = navContainer.children;
      const targetMap = {
        "Overview": createdFrames["overview"],
        "Thermal Map": createdFrames["thermal-map"],
        "Racks": createdFrames["racks"],
        "Predictions": createdFrames["predictions"],
        "AI Model": createdFrames["ai-model"],
        "Events": createdFrames["events"],
        "Datasets": createdFrames["datasets"]
      };

      links.forEach(link => {
        const txt = link.findOne(n => n.type === "TEXT");
        if (txt && targetMap[txt.characters]) {
          link.reactions = [{
            action: { type: "NODE", destinationId: targetMap[txt.characters].id, navigation: "NAVIGATE" },
            trigger: { type: "ON_CLICK" }
          }];
        }
      });
    }
  }

  figma.notify("✅ THERVO - ACM Native Figma Design Generated Successfully!");
}

generateTherVOApp();
