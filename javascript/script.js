let github_link = document.getElementById("github-link");
let linkedin_link = document.getElementById("linkedin-link");

const linkToGitHub = () => {
    window.open("{{placeholder_github}}","_blank");
};

const linkToLinkedIn = () => {
    window.open("{{placeholder_linkedin}}","_blank");
};

github_link.addEventListener("click",linkToGitHub);
linkedin_link.addEventListener("click",linkToLinkedIn);
