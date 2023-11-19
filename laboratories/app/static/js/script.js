const form = document.getElementById("find_skill")
form.addEventListener("submit", (event) => {
    event.preventDefault()
    const skill = document.getElementById("skill")
    const skill_value = skill.value
    window.location.pathname="/skills/" + skill_value
})