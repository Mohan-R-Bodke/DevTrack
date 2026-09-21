document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       Auto-hide alerts
       ========================= */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 3000);

    });


    /* =========================
       Delete confirmation modal
       ========================= */

    const modal = document.getElementById("deleteModal");
    const deleteForm = document.getElementById("deleteForm");
    const cancelButton = document.getElementById("cancelDelete");
    const itemName = document.getElementById("deleteItemName");

    const deleteButtons = document.querySelectorAll(".delete-btn");


    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const name = button.getAttribute("data-name");
            const action = button.getAttribute("data-action");

            itemName.textContent = name;
            deleteForm.action = action;

            modal.classList.add("active");

        });

    });


    /* Cancel */

    if (cancelButton) {

        cancelButton.addEventListener("click", function () {

            modal.classList.remove("active");

        });

    }


    /* Click outside popup */

    if (modal) {

        modal.addEventListener("click", function (event) {

            if (event.target === modal) {

                modal.classList.remove("active");

            }

        });

    }

});