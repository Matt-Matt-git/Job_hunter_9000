

// this variable is shared between both filters
let activeStatus = "all"

function applyFilters() {
    let search_value = document.getElementById("search").value.toLowerCase()
    let rows = document.querySelectorAll(".tablerow_job")
    
    rows.forEach(row => {
        let companyCell = row.cells[0].textContent.toLowerCase()
        let roleCell = row.cells[1].textContent.toLowerCase()
        let statusCell = row.cells[2].textContent.toLowerCase()
        
        let matchesSearch = companyCell.includes(search_value) || roleCell.includes(search_value)
        let matchesStatus = activeStatus === "all" || statusCell === activeStatus
        
        if (matchesSearch && matchesStatus) {
            row.style.display = ""
        } else {
            row.style.display = "none"
        }
    })
}

// status filter updates activeStatus then runs applyFilters
function filterStatus(status) {
    activeStatus = status
    let buttons = document.querySelectorAll(".filter_button")
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

function openDialog() {
    document.getElementById("add_dialog").showModal()
}

function closeDialog() {
    document.getElementById("add_dialog").close()
}

function openEditDialog(index, company, title, status, date, notes) {
    document.getElementById("edit_index").value = index
    document.getElementById("edit_company").value = company
    document.getElementById("edit_title").value = title
    document.getElementById("edit_status").value = status
    document.getElementById("edit_date").value = date
    document.getElementById("edit_notes").value = notes
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
        labels: ["Applied", "Interview", "Rejected"],
        datasets: [{
            data: [applied, interview, rejected],
            backgroundColor: ["#4CAF50", "#FF9800", "#f44336"]
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
            title: {
                display: true,
                text: "Number of Applications",
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
