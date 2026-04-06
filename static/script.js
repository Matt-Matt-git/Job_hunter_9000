

// this variable is shared between both filters
let activeStatus = "all"
let activeIndustry = "all"
let activeSource = "all"

function applyFilters() {
    let search_value = document.getElementById("search").value.toLowerCase()
    let rows = document.querySelectorAll(".tablerow_job")
    
    rows.forEach(row => {
        let companyCell = row.cells[0].textContent.toLowerCase()
        let roleCell = row.cells[1].textContent.toLowerCase()
        let statusCell = row.cells[2].textContent.toLowerCase()

        let industryMatch = activeIndustry === "all" || row.dataset.industry === activeIndustry
        let sourceMatch = activeSource === "all" || row.dataset.source === activeSource

        
        let matchesSearch = companyCell.includes(search_value) || roleCell.includes(search_value)
        let matchesStatus = activeStatus === "all" || statusCell === activeStatus
        
        if (matchesSearch && matchesStatus && industryMatch && sourceMatch) {
            row.style.display = ""
        } else {
            row.style.display = "none"
        }
    })
}

// status filter updates activeStatus then runs applyFilters
function filterStatus(status) {
    activeStatus = status
    let buttons = document.querySelectorAll("#status_filter_bar .filter_button")
    buttons.forEach(button => button.classList.remove("active"))
    event.target.classList.add("active")
    applyFilters()
}

function filterIndustry(industry) {
    activeIndustry = industry
    let buttons = document.querySelectorAll("#industry_filter_bar .filter_button")
    buttons.forEach(button => button.classList.remove("active"))
    event.target.classList.add("active")
    applyFilters()
}

function filterSource(source) {
    activeSource = source
    let buttons = document.querySelectorAll("#source_filter_bar .filter_button")
    buttons.forEach(button => button.classList.remove("active"))
    event.target.classList.add("active")
    applyFilters()
}

// search listener just runs applyFilters
document.getElementById("search").addEventListener("input", function() {
    applyFilters()
})

function changeTimeframe(timeframe) {
    if (timeframe === "M") {
        timeChart.data.labels = chartLabelsM
        timeChart.data.datasets[0].data = chartDataM
    } else if (timeframe === "W") {
        timeChart.data.labels = chartLabelsW
        timeChart.data.datasets[0].data = chartDataW
    } else if (timeframe === "D") {
        timeChart.data.labels = chartLabelsD
        timeChart.data.datasets[0].data = chartDataD
    }
    timeChart.update()
}

let currentSort = { column: null, ascending: true }

function sortTable(columnIndex) {
    let rows = Array.from(document.querySelectorAll(".tablerow_job"))
    if (currentSort.column === columnIndex) {
        currentSort.ascending = !currentSort.ascending  // flip direction
    } else {
        currentSort.column = columnIndex
        currentSort.ascending = true  // reset to ascending for new column
    }
    rows.sort((a, b) => {
    let aText = a.cells[columnIndex].textContent.trim()
    let bText = b.cells[columnIndex].textContent.trim()

    let aDate = Date.parse(aText)
    let bDate = Date.parse(bText)
    let comparison
    if (!isNaN(aDate) && !isNaN(bDate)) {
        comparison = aDate - bDate  // numeric date comparison
    } else {
        comparison = aText.localeCompare(bText)  // string comparison
    }
    return currentSort.ascending ? comparison : -comparison
})
    let table = document.querySelector(".maintable")
    rows.forEach(row => table.appendChild(row))
}

function openDialog() {
    document.getElementById("add_dialog").showModal()
}

function closeDialog() {
    document.getElementById("add_dialog").close()
}

function openEditDialog(index, data) {
    document.getElementById("edit_index").value = index
    document.getElementById("edit_company").value = data.company || ""
    document.getElementById("edit_title").value = data.title || ""
    document.getElementById("edit_status").value = data.status || ""
    document.getElementById("edit_date").value = data.date || ""
    document.getElementById("edit_industry").value = data.industry || ""
    document.getElementById("edit_source").value = data.source || ""
    document.getElementById("edit_contact_name").value = data.contactName || ""
    document.getElementById("edit_contact_email").value = data.contactEmail || ""
    document.getElementById("edit_salary").value = data.salary || ""
    document.getElementById("edit_job_url").value = data.jobUrl || ""
    document.getElementById("edit_location").value = data.location || ""
    document.getElementById("edit_closing_date").value = data.closingDate || ""
    document.getElementById("edit_notes").value = data.notes || ""
    document.getElementById("edit_dialog").showModal()
}

function closeEditDialog() {
    document.getElementById("edit_dialog").close()
}

function openDetailsDialog(data) {
    document.getElementById("details_company").textContent = data.company
    document.getElementById("details_job_title").textContent = data.jobTitle
    document.getElementById("details_status").textContent = data.status
    document.getElementById("details_date").textContent = data.date
    document.getElementById("details_industry").textContent = data.industry
    document.getElementById("details_source").textContent = data.source
    document.getElementById("details_location").textContent = data.location
    document.getElementById("details_salary").textContent = data.salary
    document.getElementById("details_contact").textContent = data.contactName + " — " + data.contactEmail
    document.getElementById("details_closing_date").textContent = data.closingDate
    document.getElementById("details_notes").textContent = data.notes
    document.getElementById("details_url").href = data.jobUrl
    document.getElementById("details_dialog").showModal()
    
    let urlButton = document.getElementById("details_url")
    if (data.jobUrl) {
       urlButton.href = data.jobUrl
       urlButton.style.display = ""
    } else {
       urlButton.style.display = "none"
    }
}

function closeDetailsDialog() {
    document.getElementById("details_dialog").close()
}

const ctx = document.getElementById("statusChart")
new Chart(ctx, {
    type: "doughnut",
    data: {
        labels: ["Applied", "Interview", "Rejected", "Offer", "Withdrawn"],
        datasets: [{
            data: [applied, interview, rejected, offers, withdrawn],
            backgroundColor: ["#4CAF50", "#FF9800", "#f44336", "#36d1f4ff", "#de55f3ff"]
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom"  // moves the legend to the bottom
            },
            title: {
                display: true,
                text: "Application Status",
                font: {
                    size: 18,
                    weight: "bold"
                },
                color: "#1D3A50",
                padding: {
                    bottom: 16
                }
            }
        }
    }
})

const sourceColors = {
    "LinkedIn": "#0077B5",        // LinkedIn blue
    "Indeed": "#FF6B35",          // Indeed orange
    "Company Website": "#4CAF50", // green
    "Friend/Referral": "#9C27B0", // purple
    "Recruiter": "#1D3A50",       // dark blue
    "Other": "#91A1AC"            // grey
}

const bar = document.getElementById("app_bar")
let timeChart = new Chart(bar, { 
    type: "bar",  // change to line while we're here
    data: {
        labels: chartLabelsM,  // default to monthly
        datasets: [{
            label: "Applications",
            data: chartDataM,
            backgroundColor: "#4CAF50",
            borderColor: "#4CAF50"
        }]
    },    
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom"  // moves the legend to the bottom
            },
            title: {
                display: true,
                text: "Number of Application",
                font: {
                    size: 18,
                    weight: "bold"
                },
                color: "#1D3A50",
                padding: {
                    bottom: 16
                }
            }
        }
    }
})



const sourceCtx = document.getElementById("sourceChart")
new Chart(sourceCtx, {
    type: "doughnut",
    data: {
        labels: sourceLabels,
        datasets: [{
            data: sourceData,
            backgroundColor: sourceLabels.map(label => sourceColors[label] || "#91A1AC")
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom"  // moves the legend to the bottom
            },
            title: {
                display: true,
                text: "Job Source",
                font: {
                    size: 18,
                    weight: "bold"
                },
                color: "#1D3A50",
                padding: {
                    bottom: 16
                }
            }
        }
    }
})

console.log(sourceSuccessData)
console.log(sourceSuccessLabels)

const successSourceCtx = document.getElementById("successSource_bar")
new Chart(successSourceCtx, {
    type: "bar",
    data: {
        labels: sourceSuccessLabels,
        datasets: [{
            data: sourceSuccessData,
            backgroundColor: sourceLabels.map(label => sourceColors[label] || "#91A1AC"),
            borderColor: sourceLabels.map(label => sourceColors[label] || "#91A1AC")
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
            position: "bottom",
            labels: {
                generateLabels: function(chart) {
                    return sourceSuccessLabels.map((label, index) => ({
                        text: label,
                        fillStyle: sourceColors[label] || "#91A1AC",
                        strokeStyle: sourceColors[label] || "#91A1AC",
                        lineWidth: 1,
                        hidden: false,
                        index: index
                    }));
                }
            },
                position: "bottom"  // moves the legend to the bottom
            },
            title: {
                display: true,
                text: "Interview rate by Source",
                font: {
                    size: 18,
                    weight: "bold"
                },
                color: "#1D3A50",      
                padding: {
                    bottom: 16
                }
            }
        }
    }
})

const industryColors = {
    "Pharmaceutical": "#E63946",    // red
    "Biotech": "#2A9D8F",           // teal
    "Chemical": "#E9C46A",          // yellow
    "Food & Beverage": "#F4A261",   // orange
    "Finance": "#1D3A50",           // dark blue
    "Technology": "#4361EE",        // bright blue
    "Retail": "#7209B7",            // purple
    "Hospitality": "#F72585",       // pink
    "Healthcare": "#4CC9F0",        // light blue
    "Academic/Research": "#3A0CA3", // deep purple
    "Engineering": "#80B918",       // green
    "Legal": "#6D6875",             // mauve
    "Marketing": "#FF6B6B",         // coral
    "Other": "#91A1AC"              // grey
}

const industryCtx = document.getElementById("industryChart")
new Chart(industryCtx, {
    type: "doughnut",
    data: {
        labels: industryLabels,
        datasets: [{
            data: industryData,
            backgroundColor: industryLabels.map(label => industryColors[label] || "#91A1AC")
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom"  // moves the legend to the bottom
            },
            title: {
                display: true,
                text: "Application by Industry",
                font: {
                    size: 18,
                    weight: "bold"
                },
                color: "#1D3A50",
                padding: {
                    bottom: 16
                }
            }
        }
    }
})