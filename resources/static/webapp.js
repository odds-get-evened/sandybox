import van from "./van-1.5.2.min.js";

const {a, div, li, p, ul} = van.tags;

const Hello = () => div(
    p("hello"),
    ul(
        li("world"),
        li(a({href: "https://vanjs.org/"}, "vanjs"))
    )
);
van.add(document.getElementById('appRoot'), Hello());