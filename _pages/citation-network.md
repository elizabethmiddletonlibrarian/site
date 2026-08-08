---
title: "Citation Network"
permalink: /citation-network/
author_profile: false
layout: single
---

<style>

body {
    font-family: Arial, sans-serif;
}

#cy {
    width: 100%;
    height: 800px;
    border: 2px solid #e4e8ff;
    background-color: #ffffff;
    margin-top: 20px;
}

.legend {
    margin: 20px 0;
    padding: 15px;
    background-color: white;
    border: 1px solid #e4e8ff;
}

.legend-item {
    display: inline-block;
    margin-right: 20px;
}

.legend-color {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 5px;
    vertical-align: middle;
    border: 1px solid #333;
}

.legend-icon {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 5px;
    vertical-align: middle;
    border: 1px solid #333;
    background-color: #ffffff;
    background-size: 70%;
    background-repeat: no-repeat;
    background-position: center;
}

#tooltip {
    position: absolute;
    background-color: rgba(0,0,0,.85);
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 13px;
    pointer-events: none;
    display: none;
    max-width: 400px;
    z-index: 9999;
}

</style>

<h2>Citation Network Visualization</h2>

<div class="legend" id="typeLegend">
<div class="legend-item">
Node shape: <strong>Square</strong> = Pamphlet, <strong>Circle</strong> = Source  cited/referenced in pamphlet
</div>
</div>

<div class="legend" id="categoryLegend">
<strong style="display:block; margin-bottom:8px;">Source Theme</strong>
</div>

<div id="cy"></div>

<div id="tooltip"></div>

<script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
<script>
async function loadNetwork() {
    // 1. Fetch the data - using site prefix for GitHub Pages subdirectory
    const nodesUrl = "https://github.com/elizabethmiddletonlibrarian/site/assets/citation-network/nodes.json";
    const edgesUrl = "https://github.com/elizabethmiddletonlibrarian/site/assets/citation-network/edges.json";

    console.log("Loading nodes from:", nodesUrl);
    console.log("Loading edges from:", edgesUrl);

    const rawNodes = await fetch(nodesUrl).then(res => res.json());
    const rawEdges = await fetch(edgesUrl).then(res => res.json());

    // 2. CLEAN THE DATA (Removes BOM from both nodes and edges)
    const nodesData = rawNodes.map(node => {
        const cleanNode = {};
        Object.keys(node).forEach(key => {
            const cleanKey = key.replace(/[^\x20-\x7E]/g, '').trim();
            cleanNode[cleanKey] = node[key];
        });
        return cleanNode;
    });

    const edgesData = rawEdges.map(edge => {
        const cleanEdge = {};
        Object.keys(edge).forEach(key => {
            const cleanKey = key.replace(/[^\x20-\x7E]/g, '').trim();
            cleanEdge[cleanKey] = edge[key];
        });
        return cleanEdge;
    });

    const elements = [];

    // 3. MAP EACH CATEGORY TO A BROADER THEME
    // (Grouped per the Codebook's Source Category definitions)
    const categoryToTheme = {
        "British Statute": "Legal & Governmental",
        "Constitutional Document": "Legal & Governmental",
        "Convention Document": "Legal & Governmental",
        "Law Reports": "Legal & Governmental",
        "Legislative Proceedings": "Legal & Governmental",
        "Treaties, Capitulations, and Diplomatic Instruments": "Legal & Governmental",
        "Religious Text": "Religious & Spiritual",
        "Religious Tract": "Religious & Spiritual",
        "Spiritual Work": "Religious & Spiritual",
        "Enlightenment Text": "Enlightenment Text",
        "Classic Text": "Classical Text",
        "Literary Work": "Literary & Media",
        "Newspaper": "Literary & Media",
        "Historical Records": "Historical Records"
    };
    const UNCATEGORIZED = "Uncategorized";

    function themeFor(category) {
        if (!category || category.trim() === "") return UNCATEGORIZED;
        return categoryToTheme[category] || UNCATEGORIZED;
    }

    // 4. THEME ICON SET (inline SVGs encoded as data URIs)
    function svgIcon(pathMarkup) {
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${pathMarkup}</svg>`;
        return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
    }

    const themeIconMap = {
        "Legal & Governmental": svgIcon(`
            <line x1="12" y1="3" x2="12" y2="21"></line>
            <line x1="5" y1="7" x2="19" y2="7"></line>
            <path d="M5 7 L2 14 a3 3 0 0 0 6 0 Z"></path>
            <path d="M19 7 L16 14 a3 3 0 0 0 6 0 Z"></path>
            <line x1="8" y1="21" x2="16" y2="21"></line>
        `),
        "Religious & Spiritual": svgIcon(`
            <line x1="12" y1="2" x2="12" y2="22"></line>
            <line x1="6" y1="8" x2="18" y2="8"></line>
        `),
        "Enlightenment Text": svgIcon(`
            <path d="M12 4 C9 3 5 3 3 4 V19 C5 18 9 18 12 19 C15 18 19 18 21 19 V4 C19 3 15 3 12 4 Z"></path>
            <line x1="12" y1="4" x2="12" y2="19"></line>
        `),
        "Classical Text": svgIcon(`
            <line x1="3" y1="21" x2="21" y2="21"></line>
            <line x1="4" y1="4" x2="20" y2="4"></line>
            <polygon points="4,4 20,4 18,7 6,7"></polygon>
            <line x1="7" y1="7" x2="7" y2="19"></line>
            <line x1="11" y1="7" x2="11" y2="19"></line>
            <line x1="13" y1="7" x2="13" y2="19"></line>
            <line x1="17" y1="7" x2="17" y2="19"></line>
            <line x1="5" y1="19" x2="19" y2="19"></line>
        `),
        "Literary & Media": svgIcon(`
            <rect x="3" y="5" width="18" height="15" rx="1"></rect>
            <line x1="6" y1="9" x2="18" y2="9"></line>
            <line x1="6" y1="12.5" x2="18" y2="12.5"></line>
            <line x1="6" y1="16" x2="13" y2="16"></line>
        `),
        "Historical Records": svgIcon(`
            <path d="M20 4 C14 5 8 9 5 16 L4 20 L8 19 C15 16 19 10 20 4 Z"></path>
            <line x1="4" y1="20" x2="9.5" y2="14.5"></line>
        `),
        [UNCATEGORIZED]: svgIcon(`
            <circle cx="12" cy="12" r="9"></circle>
            <path d="M9.5 9.5 a2.5 2.5 0 1 1 3.5 2.3 c-1 0.6 -1 1.2 -1 2.2"></path>
            <line x1="12" y1="17" x2="12" y2="17"></line>
        `)
    };

    const themes = Object.values(themeIconMap).length
        ? [...new Set(nodesData.map(node => themeFor(node.Category)))].sort()
        : [];

    // 5. POPULATE THEME LEGEND
    const categoryLegendEl = document.getElementById("categoryLegend");
    categoryLegendEl.innerHTML = '<strong style="display:block; margin-bottom:8px;">Source Theme</strong>';
    themes.forEach(theme => {
        const item = document.createElement("div");
        item.className = "legend-item";
        item.innerHTML = `<span class="legend-icon" style="background-image:url('${themeIconMap[theme]}')"></span>${theme}`;
        categoryLegendEl.appendChild(item);
    });

    // 6. ADD NODES (Using CLEANED keys)
    nodesData.forEach(node => {
        elements.push({
            data: {
                id: node.ID,
                label: node.Name,
                type: node.Node_Type ? node.Node_Type.toLowerCase() : "source",
                year: node["Publication Date"],
                author_origin: node.Author_Location,
                notes: node.Notes,
                category: node.Category,
                theme: themeFor(node.Category)
            }
        });
    });

    // 7. ADD EDGES (Using CLEANED keys)
    edgesData.forEach(edge => {
        elements.push({
            data: {
                id: edge.Source + "-" + edge.Target,
                source: edge.Source,
                target: edge.Target,
                weight: Number(edge.Weight_NumOfCite) || 1,
                citation_method: edge.Citation_Method,
                description: edge.Notes
            }
        });
    });

    // 8. INITIALIZE CYTOSCAPE (ONLY ONCE, INSIDE THE FUNCTION)
    const cy = cytoscape({
        container: document.getElementById("cy"),
        elements: elements,
        style: [
            {
                selector: "node",
                style: {
                    "label": "data(label)",
                    "text-valign": "center",
                    "text-halign": "center",
                    "font-size": "11px",
                    "font-weight": 600,
                    "color": "#1a1f36",
                    "text-wrap": "wrap",
                    "text-max-width": "100px",
                    "width": 120,
                    "height": 120,
                    "border-width": 2.5,
                    "border-color": "#2c3454",
                    "background-color": "#eef1f8"
                }
            },
            {
                selector: 'node[type="pamphlet"]',
                style: {
                    "shape": "rectangle",
                    "width": 170,
                    "height": 170,
                    "text-max-width": "150px",
                    "background-image": "none"
                }
            },
            {
                selector: 'node[type="source"]',
                style: {
                    "shape": "ellipse",
                    "width": 170,
                    "height": 170,
                    "text-valign": "center",
                    "text-halign": "center",
                    "text-margin-y": -34,
                    "background-image": function(ele) {
                        return themeIconMap[ele.data("theme")] || themeIconMap[UNCATEGORIZED];
                    },
                    "background-fit": "none",
                    "background-clip": "node",
                    "background-width": "68px",
                    "background-height": "68px",
                    "background-position-x": "50%",
                    "background-position-y": "72%",
                    "text-max-width": "150px"
                }
            },
            {
                selector: "edge",
                style: {
                    "width": "mapData(weight, 1, 28, 1.5, 10)",
                    "line-color": "#6b7280",
                    "target-arrow-color": "#6b7280",
                    "target-arrow-shape": "triangle",
                    "arrow-scale": 1.2,
                    "curve-style": "bezier",
                    "opacity": 0.9
                }
            },
            {
                selector: ".faded",
                style: {
                    "opacity": 0.15
                }
            },
            {
                selector: "edge.highlighted",
                style: {
                    "line-color": "#e63946",
                    "target-arrow-color": "#e63946",
                    "opacity": 1,
                    "z-index": 999
                }
            },
            {
                selector: "node.highlighted",
                style: {
                    "border-color": "#e63946",
                    "border-width": 4,
                    "opacity": 1,
                    "z-index": 999
                }
            }
        ],
        layout: {
            name: "cose",
            animate: true,
            idealEdgeLength: 220,
            nodeRepulsion: 18000,
            nodeOverlap: 20,
            componentSpacing: 120,
            gravity: 60
        }
    });

    // 9. TOOLTIP FUNCTIONALITY
    const tooltip = document.getElementById("tooltip");

    cy.on("mouseover", "node", function(event) {
        const node = event.target;
        const data = node.data();

        tooltip.innerHTML =
            "<strong>" + data.label + "</strong><br>" +
            (data.year ? "Year: " + data.year + "<br>" : "") +
            (data.category ? "Category: " + data.category + "<br>" : "") +
            (data.theme && data.type !== "pamphlet" ? "Theme: " + data.theme + "<br>" : "") +
            (data.author_origin ? "Origin: " + data.author_origin : "");

        tooltip.style.display = "block";

        // Highlight connected edges and neighbor nodes
        const connectedEdges = node.connectedEdges();
        const neighborhood = connectedEdges.connectedNodes().union(node);

        cy.elements().addClass("faded");
        neighborhood.removeClass("faded");
        connectedEdges.removeClass("faded");
        connectedEdges.addClass("highlighted");
        node.addClass("highlighted");
    });

    cy.on("mouseout", "node", function(event) {
        cy.elements().removeClass("faded highlighted");
    });

    cy.on("mouseover", "edge", function(event) {
        const data = event.target.data();

        tooltip.innerHTML =
            "<strong>Reference</strong><br>" +
            (data.citation_method ? "Method: " + data.citation_method + "<br>" : "") +
            (data.weight ? "Number of Mentions: " + data.weight + "<br>" : "") +
            (data.description ? data.description : "");

        tooltip.style.display = "block";
    });

    cy.on("mouseout", "node, edge", function() {
        tooltip.style.display = "none";
    });

    cy.on("mousemove", function(event) {
        tooltip.style.left = (event.originalEvent.pageX + 10) + "px";
        tooltip.style.top = (event.originalEvent.pageY + 10) + "px";
    });
}

loadNetwork();
</script>
