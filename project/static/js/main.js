let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e)=>{
        let arrowParent = e.target.parentElement.parentElement;
        arrowParent.classList.toggle("showMenu");
    });
}

function closeAside() {
    sidebar.classList.toggle("close");
}

let sidebar = document.querySelector("aside");

let sidebarBtn = document.querySelector(".bx-chevron-left")
sidebarBtn.addEventListener("click", closeAside);

let sidebarMenuBtn = document.querySelector(".bx-menu");
sidebarMenuBtn.addEventListener("click", closeAside);

let sidebarCloseBtn = document.querySelector("aside .bx-x")
sidebarCloseBtn.addEventListener("click", closeAside);
