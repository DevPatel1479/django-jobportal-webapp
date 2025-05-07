function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    console.log("button pressed");
    const icon = document.querySelector('.theme-toggle i');
    icon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
}
