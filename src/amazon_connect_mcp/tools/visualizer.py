"""Layout visualizer - generates standalone HTML file."""

import json
import tempfile
import webbrowser
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "cases"


def generate_html() -> str:
    """Generate the layout visualizer HTML page."""
    
    # Load all industry templates
    industries = {}
    for f in TEMPLATES_DIR.glob("*.json"):
        if not f.name.startswith("_"):
            with open(f) as file:
                data = json.load(file)
                custom_fields = data.get("customFields", [])
                
                # Handle both array and object formats for customFields
                if isinstance(custom_fields, dict):
                    # Convert object format to array format
                    fields = [
                        {"name": name, "type": field_def.get("type", "Text")}
                        for name, field_def in custom_fields.items()
                    ]
                else:
                    # Already in array format
                    fields = custom_fields
                
                industries[f.stem] = {
                    "name": data.get("name", f.stem),
                    "fields": fields
                }
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Connect Cases - Layout Builder</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }}
        
        .header {{ background: #232f3e; color: white; padding: 12px 24px; display: flex; align-items: center; gap: 16px; }}
        .header h1 {{ font-size: 18px; font-weight: 500; }}
        
        .container {{ display: grid; grid-template-columns: 260px 1fr 380px; height: calc(100vh - 52px); }}
        
        /* Fields Panel */
        .fields-panel {{ background: white; border-right: 1px solid #e1e4e8; padding: 16px; overflow-y: auto; }}
        .fields-panel h2 {{ font-size: 12px; color: #545b64; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        .industry-select {{ width: 100%; padding: 8px; margin-bottom: 16px; border: 1px solid #d5dbdb; border-radius: 4px; font-size: 13px; }}
        
        .field-item {{ background: #f9fafb; border: 1px solid #e1e4e8; border-radius: 4px; padding: 8px 10px; margin-bottom: 6px; cursor: grab; display: flex; justify-content: space-between; align-items: center; transition: all 0.15s; font-size: 13px; }}
        .field-item:hover {{ background: #eef6ff; border-color: #0073bb; }}
        .field-item.dragging {{ opacity: 0.5; }}
        .field-item.used {{ opacity: 0.4; background: #e9ebed; }}
        .field-name {{ font-weight: 500; color: #16191f; display: flex; align-items: center; gap: 8px; }}
        .drag-handle {{ color: #aab7b8; font-size: 14px; cursor: grab; }}
        .field-item:hover .drag-handle {{ color: #0073bb; }}
        .field-type {{ font-size: 10px; color: #687078; background: #e9ebed; padding: 2px 5px; border-radius: 3px; }}
        
        .system-fields {{ margin-top: 20px; padding-top: 16px; border-top: 1px solid #e1e4e8; }}
        .system-fields .field-item {{ background: #fff8e6; border-color: #f0c14b; }}
        .system-fields .field-item.used {{ background: #f5f0e0; }}
        
        .hint {{ font-size: 11px; color: #687078; margin-top: 12px; font-style: italic; }}
        
        /* Preview Panel - Amazon Connect Style */
        .preview-panel {{ background: #f9fafb; padding: 20px; overflow-y: auto; }}
        .preview-panel > h2 {{ font-size: 12px; color: #545b64; margin-bottom: 12px; text-transform: uppercase; }}
        
        .case-preview {{ background: white; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.08); overflow: hidden; border: 1px solid #e1e4e8; }}
        
        /* Case Header - like Connect */
        .case-header {{ padding: 16px 20px; border-bottom: 1px solid #eaeded; }}
        .case-title {{ font-size: 20px; font-weight: 600; color: #16191f; margin-bottom: 12px; }}
        .case-actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .case-action {{ display: inline-flex; align-items: center; gap: 4px; padding: 6px 12px; border: 1px solid #d5dbdb; border-radius: 4px; font-size: 13px; color: #16191f; background: white; cursor: default; }}
        .case-action.status {{ background: #f9fafb; }}
        .case-action.status::after {{ content: '▾'; margin-left: 4px; font-size: 10px; }}
        
        /* Summary Section */
        .summary-section {{ padding: 16px 20px; border-bottom: 1px solid #eaeded; }}
        .summary-label {{ font-size: 13px; font-weight: 600; color: #16191f; margin-bottom: 4px; }}
        .summary-label a {{ color: #0073bb; font-weight: 400; margin-left: 4px; text-decoration: none; }}
        .summary-text {{ font-size: 14px; color: #16191f; line-height: 1.5; }}
        
        /* Top Panel - Two Column Grid */
        .top-panel-section {{ padding: 16px 20px; border-bottom: 1px solid #eaeded; }}
        .panel-label {{ font-size: 11px; color: #687078; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }}
        
        .drop-zone {{ min-height: 60px; border: 2px dashed #d5dbdb; border-radius: 4px; padding: 12px; transition: all 0.2s; display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; }}
        .drop-zone.drag-over {{ border-color: #0073bb; background: #f0f8ff; }}
        .drop-zone.empty {{ display: flex; align-items: center; justify-content: center; color: #aab7b8; font-size: 12px; }}
        .drop-zone:not(.empty) {{ border: 1px solid #e1e4e8; background: #fafafa; }}
        
        .drop-placeholder {{ grid-column: 1 / -1; border: 2px dashed #d5dbdb; border-radius: 4px; padding: 16px; text-align: center; color: #aab7b8; font-size: 12px; min-height: 50px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }}
        .drop-placeholder:hover {{ border-color: #0073bb; background: #f0f8ff; }}
        
        .field-in-panel {{ cursor: move; transition: all 0.15s; padding: 8px; border-radius: 4px; background: white; border: 1px solid #e1e4e8; }}
        .field-in-panel:hover {{ background: #f0f8ff; border-color: #0073bb; }}
        .field-in-panel.drag-over {{ border-left: 3px solid #0073bb; }}
        .field-label {{ font-size: 12px; color: #545b64; margin-bottom: 2px; display: flex; align-items: center; gap: 6px; }}
        .field-label .drag-handle {{ color: #aab7b8; font-size: 12px; }}
        .field-in-panel:hover .drag-handle {{ color: #0073bb; }}
        .field-value {{ font-size: 14px; color: #16191f; display: flex; justify-content: space-between; align-items: center; }}
        .field-value .remove-btn {{ color: #d13212; cursor: pointer; font-size: 14px; opacity: 0; padding: 2px 6px; }}
        .field-in-panel:hover .remove-btn {{ opacity: 0.6; }}
        .field-value .remove-btn:hover {{ opacity: 1; }}
        .field-value a {{ color: #0073bb; text-decoration: none; }}
        
        /* Tabs - like Connect */
        .tabs {{ display: flex; border-bottom: 1px solid #eaeded; padding: 0 20px; }}
        .tab {{ padding: 12px 16px; cursor: pointer; font-size: 14px; color: #545b64; border-bottom: 2px solid transparent; margin-bottom: -1px; }}
        .tab.active {{ color: #0073bb; border-bottom-color: #0073bb; }}
        .tab-content {{ display: none; padding: 16px 20px; }}
        .tab-content.active {{ display: block; }}
        
        /* More Info Section */
        .more-info-section {{ padding: 16px 20px; }}
        
        /* JSON Panel */
        .json-panel {{ background: #1e1e1e; color: #d4d4d4; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; }}
        .json-panel h2 {{ font-size: 12px; color: #888; margin-bottom: 8px; text-transform: uppercase; }}
        
        .output-section {{ flex: 1; display: flex; flex-direction: column; min-height: 0; }}
        .output-section h3 {{ font-size: 11px; color: #888; margin-bottom: 6px; text-transform: uppercase; }}
        .json-output {{ flex: 1; font-family: 'Monaco', 'Menlo', 'Consolas', monospace; font-size: 11px; line-height: 1.5; white-space: pre-wrap; background: #252526; padding: 12px; border-radius: 4px; overflow-y: auto; min-height: 100px; }}
        
        .copy-btn {{ background: #0073bb; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 12px; margin-bottom: 12px; }}
        .copy-btn:hover {{ background: #005a8c; }}
        
        .api-section {{ flex: 1; display: flex; flex-direction: column; min-height: 0; border-top: 1px solid #333; padding-top: 12px; }}
        .api-section code {{ flex: 1; display: block; background: #252526; padding: 12px; border-radius: 4px; font-size: 11px; white-space: pre-wrap; overflow-y: auto; font-family: 'Monaco', 'Menlo', 'Consolas', monospace; min-height: 100px; }}
    </style>
</head>
<body>
    <div class="header">
        <svg width="28" height="28" viewBox="0 0 32 32" fill="none"><path d="M16 4L4 10v12l12 6 12-6V10L16 4z" fill="#FF9900"/><path d="M16 16v12l12-6V10L16 16z" fill="#FFB84D"/></svg>
        <h1>Amazon Connect Cases - Layout Builder</h1>
    </div>
    
    <div class="container">
        <div class="fields-panel">
            <h2>Available Fields</h2>
            <select class="industry-select" id="industrySelect" onchange="loadIndustry(this.value)">
                {"".join(f'<option value="{k}">{v["name"]}</option>' for k, v in sorted(industries.items(), key=lambda x: x[1]["name"]))}
            </select>
            
            <div id="customFields"></div>
            
            <div class="system-fields">
                <h2>System Fields</h2>
                <div class="field-item" draggable="true" data-field-id="customer_id" data-field-name="Customer name" data-field-type="System">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>Customer name</span>
                    <span class="field-type">System</span>
                </div>
                <div class="field-item" draggable="true" data-field-id="created_datetime" data-field-name="Date created" data-field-type="System">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>Date created</span>
                    <span class="field-type">System</span>
                </div>
                <div class="field-item" draggable="true" data-field-id="last_updated_datetime" data-field-name="Last updated" data-field-type="System">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>Last updated</span>
                    <span class="field-type">System</span>
                </div>
                <div class="field-item" draggable="true" data-field-id="case_reason" data-field-name="Case Reason" data-field-type="System">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>Case Reason</span>
                    <span class="field-type">System</span>
                </div>
                <div class="field-item" draggable="true" data-field-id="reference_number" data-field-name="Reference Number" data-field-type="System">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>Reference Number</span>
                    <span class="field-type">System</span>
                </div>
            </div>
            <p class="hint">💡 Drag fields to panels. Drag within panels to reorder.</p>
        </div>
        
        <div class="preview-panel">
            <h2>Case Preview</h2>
            <div class="case-preview">
                <!-- Case Header -->
                <div class="case-header">
                    <div class="case-title">Windshield damage – claim</div>
                    <div class="case-actions">
                        <span class="case-action status">Status: Closed</span>
                        <span class="case-action">+ Task</span>
                        <span class="case-action">✎ Edit</span>
                        <span class="case-action">Assign to</span>
                        <span class="case-action">Audit history</span>
                    </div>
                </div>
                
                <!-- Summary Section -->
                <div class="summary-section">
                    <div class="summary-label">Summary <a href="#">Info</a></div>
                    <div class="summary-text">Customer was driving on i90 on the way back from work, and a small rock hit their windshield.</div>
                </div>
                
                <!-- Top Panel Fields - Two Column -->
                <div class="top-panel-section">
                    <div class="panel-label">Top Panel Fields (Always Visible)</div>
                    <div class="drop-zone empty" id="topPanel" data-panel="topPanel">
                        Drag fields here – displays in 2 columns
                    </div>
                </div>
                
                <!-- Tabs -->
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('activity')">Activity feed</div>
                    <div class="tab" onclick="switchTab('comments')">Comments</div>
                    <div class="tab" onclick="switchTab('moreInfo')">More information</div>
                </div>
                
                <div class="tab-content active" id="activityTab">
                    <div style="color: #687078; font-size: 13px; text-align: center; padding: 30px;">
                        <div style="margin-bottom: 8px;">📞 Inbound call</div>
                        <div style="font-size: 12px;">March 12, 2024, 11:48 AM</div>
                    </div>
                </div>
                
                <div class="tab-content" id="commentsTab">
                    <div style="color: #687078; font-size: 13px; text-align: center; padding: 30px;">No comments yet</div>
                </div>
                
                <div class="tab-content" id="moreInfoTab">
                    <div class="panel-label">More Information Fields</div>
                    <div class="drop-zone empty" id="moreInfo" data-panel="moreInfo">
                        Drag fields here – displays in 2 columns
                    </div>
                </div>
            </div>
        </div>
        
        <div class="json-panel">
            <div class="output-section">
                <h3>Generated Layout JSON</h3>
                <div class="json-output" id="jsonOutput"></div>
                <button class="copy-btn" onclick="copyJson()">📋 Copy JSON</button>
            </div>
            
            <div class="api-section">
                <h3>MCP Tool Call</h3>
                <code id="apiCall"></code>
            </div>
        </div>
    </div>
    
    <script>
        const industries = {json.dumps(industries)};
        const layoutState = {{ topPanel: [], moreInfo: [] }};
        let draggedField = null;
        let draggedFromPanel = null;
        let draggedIndex = null;
        
        function loadIndustry(industry) {{
            const fields = industries[industry]?.fields || [];
            const container = document.getElementById('customFields');
            container.innerHTML = fields.map(f => `
                <div class="field-item" draggable="true" 
                     data-field-id="${{f.name.toLowerCase().replace(/ /g, '_')}}" 
                     data-field-name="${{f.name}}" 
                     data-field-type="${{f.type}}">
                    <span class="field-name"><span class="drag-handle">⋮⋮</span>${{f.name}}</span>
                    <span class="field-type">${{f.type}}</span>
                </div>
            `).join('');
            
            layoutState.topPanel = [];
            layoutState.moreInfo = [];
            renderPanel('topPanel');
            renderPanel('moreInfo');
            updateJson();
            updateFieldUsedState();
            initSidebarDrag();
        }}
        
        function initSidebarDrag() {{
            // Attach drag listeners to all field items in the sidebar
            document.querySelectorAll('.fields-panel .field-item').forEach(item => {{
                item.ondragstart = e => {{
                    draggedField = {{
                        id: item.dataset.fieldId,
                        name: item.dataset.fieldName,
                        type: item.dataset.fieldType
                    }};
                    draggedFromPanel = null;
                    draggedIndex = null;
                    item.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'copy';
                }};
                item.ondragend = () => {{
                    item.classList.remove('dragging');
                    draggedField = null;
                }};
            }});
        }}
        
        function setupDropZone(panelId) {{
            const zone = document.getElementById(panelId);
            if (!zone) return;
            
            zone.ondragover = e => {{
                e.preventDefault();
                e.dataTransfer.dropEffect = draggedFromPanel ? 'move' : 'copy';
                zone.classList.add('drag-over');
            }};
            
            zone.ondragleave = e => {{
                if (!zone.contains(e.relatedTarget)) {{
                    zone.classList.remove('drag-over');
                }}
            }};
            
            zone.ondrop = e => {{
                e.preventDefault();
                zone.classList.remove('drag-over');
                
                if (draggedFromPanel && draggedFromPanel !== panelId) {{
                    // Moving from one panel to another
                    const field = layoutState[draggedFromPanel][draggedIndex];
                    layoutState[draggedFromPanel].splice(draggedIndex, 1);
                    layoutState[panelId].push(field);
                    renderPanel(draggedFromPanel);
                }} else if (!draggedFromPanel && draggedField) {{
                    // Adding new field from sidebar
                    if (!layoutState[panelId].find(f => f.id === draggedField.id)) {{
                        layoutState[panelId].push({{...draggedField}});
                        updateFieldUsedState();
                    }}
                }}
                renderPanel(panelId);
                updateJson();
            }};
        }}
        
        function initPanelDrag(panel) {{
            const zone = document.getElementById(panel);
            const items = zone.querySelectorAll('.field-in-panel');
            
            items.forEach((item, index) => {{
                item.draggable = true;
                
                item.ondragstart = e => {{
                    e.stopPropagation();
                    draggedFromPanel = panel;
                    draggedIndex = index;
                    draggedField = layoutState[panel][index];
                    item.style.opacity = '0.5';
                    e.dataTransfer.effectAllowed = 'move';
                }};
                
                item.ondragend = () => {{
                    item.style.opacity = '1';
                    document.querySelectorAll('.field-in-panel').forEach(i => i.classList.remove('drag-over'));
                    draggedFromPanel = null;
                    draggedIndex = null;
                }};
                
                item.ondragover = e => {{
                    e.preventDefault();
                    e.stopPropagation();
                    if (draggedFromPanel === panel && draggedIndex !== index) {{
                        item.classList.add('drag-over');
                    }}
                }};
                
                item.ondragleave = () => item.classList.remove('drag-over');
                
                item.ondrop = e => {{
                    e.preventDefault();
                    e.stopPropagation();
                    item.classList.remove('drag-over');
                    
                    if (draggedFromPanel === panel && draggedIndex !== null && draggedIndex !== index) {{
                        const [moved] = layoutState[panel].splice(draggedIndex, 1);
                        layoutState[panel].splice(index, 0, moved);
                        renderPanel(panel);
                        updateJson();
                    }}
                }};
            }});
        }}
        
        function updateFieldUsedState() {{
            const usedIds = [...layoutState.topPanel, ...layoutState.moreInfo].map(f => f.id);
            document.querySelectorAll('.fields-panel .field-item').forEach(item => {{
                item.classList.toggle('used', usedIds.includes(item.dataset.fieldId));
            }});
        }}
        
        function removeField(panel, fieldId) {{
            layoutState[panel] = layoutState[panel].filter(f => f.id !== fieldId);
            renderPanel(panel);
            updateFieldUsedState();
            updateJson();
        }}
        
        function renderPanel(panel) {{
            const zone = document.getElementById(panel);
            if (!zone) return;
            
            if (layoutState[panel].length === 0) {{
                zone.innerHTML = '<div class="drop-placeholder">Drop fields here – displays in 2 columns</div>';
                zone.classList.add('empty');
            }} else {{
                zone.classList.remove('empty');
                const fieldsHtml = layoutState[panel].map((f, idx) => `
                    <div class="field-in-panel" data-index="${{idx}}" data-field-id="${{f.id}}">
                        <div class="field-label"><span class="drag-handle">⋮⋮</span>${{f.name}}</div>
                        <div class="field-value">
                            <span>${{f.type === 'System' ? '<a href="#">Sample Value</a>' : 'Sample Value'}}</span>
                            <span class="remove-btn" onclick="event.stopPropagation(); removeField('${{panel}}', '${{f.id}}')">&times;</span>
                        </div>
                    </div>
                `).join('');
                // Always show placeholder at the end for adding more fields
                zone.innerHTML = fieldsHtml + '<div class="drop-placeholder">+ Drop more fields</div>';
                initPanelDrag(panel);
            }}
            // Re-setup drop zone handlers after render
            setupDropZone(panel);
        }}
        
        function updateJson() {{
            const content = {{
                basic: {{
                    topPanel: {{ 
                        sections: layoutState.topPanel.length ? [{{
                            fieldGroup: {{
                                name: "Top Panel Fields",
                                fields: layoutState.topPanel.map(f => ({{ id: f.id }}))
                            }}
                        }}] : [] 
                    }},
                    moreInfo: {{ 
                        sections: layoutState.moreInfo.length ? [{{
                            fieldGroup: {{
                                name: "More Information Fields", 
                                fields: layoutState.moreInfo.map(f => ({{ id: f.id }}))
                            }}
                        }}] : [] 
                    }}
                }}
            }};
            
            const jsonStr = JSON.stringify(content, null, 2);
            document.getElementById('jsonOutput').textContent = jsonStr;
            document.getElementById('apiCall').textContent = 
`cases_create_layout(
  domain_id="your-domain-id",
  name="My Layout",
  content=${{jsonStr}}
)`;
        }}
        
        function switchTab(tab) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            const tabMap = {{ activity: 0, comments: 1, moreInfo: 2 }};
            document.querySelectorAll('.tab')[tabMap[tab]].classList.add('active');
            document.getElementById(tab + 'Tab').classList.add('active');
        }}
        
        function copyJson() {{
            const json = document.getElementById('jsonOutput').textContent;
            navigator.clipboard.writeText(json);
            const btn = document.querySelector('.copy-btn');
            btn.textContent = '✓ Copied!';
            setTimeout(() => btn.textContent = '📋 Copy JSON', 2000);
        }}
        
        // Initialize
        setupDropZone('topPanel');
        setupDropZone('moreInfo');
        loadIndustry(document.getElementById('industrySelect').value);
    </script>
</body>
</html>'''


def get_visualizer_html() -> str:
    """Return the visualizer HTML."""
    return generate_html()


def open_visualizer() -> str:
    """Save HTML to temp file and open in browser. Returns the file path."""
    html = generate_html()
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
    tmp.write(html)
    tmp.close()
    webbrowser.open(f'file://{tmp.name}')
    return tmp.name
