const dashboardTheme = {
    layout: {
        paper_bgcolor: "#07080a",
        plot_bgcolor: "#0f1114",
        font: {
            family: "system-ui, sans-serif",
            color: "#eceef1"
        },
        xaxis: {
            gridcolor: "#212530"
        },
        yaxis: {
            gridcolor: "#212530"
        },
        annotations: [
            {
                name: "watermark",
                text: "© Galselo Wrapsy " + new Date().getFullYear(),
                font: {
                    size: 12,
                    color: "#eceef1",
                },
                x: 0.01,
                y: 0.01,
                xref: "paper",
                yref: "paper",
                showarrow: false,
                opacity: 0.5
            }
        ]
    }
};