document.addEventListener("DOMContentLoaded", function() {
    const darkModeToggle = document.getElementById("darkModeToggle");
    const body = document.body;

    // بررسی وجود حالت ذخیره شده در localStorage
    const isDarkMode = localStorage.getItem("darkMode");

    if (isDarkMode === "true") {
        body.classList.add("dark"); // اگر true بود، کلاس dark رو اضافه کن
        darkModeToggle.textContent = "🌑︎";
    } else {
        body.classList.remove("dark"); // اگر false یا undefined بود، کلاس dark رو حذف کن
        darkModeToggle.textContent = "☾";
    }

    darkModeToggle.addEventListener("click", function() {
        body.classList.toggle("dark");

        const isDarkMode = body.classList.contains("dark");
        localStorage.setItem("darkMode", isDarkMode.toString()); // ذخیره مقدار در localStorage

        if (isDarkMode) {
            darkModeToggle.textContent = "🌑︎";
        } else {
            darkModeToggle.textContent = "☾";
        }
    });
});
