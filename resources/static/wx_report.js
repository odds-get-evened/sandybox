import van from "./van-1.5.2.min.js";

const {a, div, li, p, ul} = van.tags;

const ReportFrame = () => {
    const counter = van.state(0);

    return div(
        button({class: 'btn btn-primary', onclick: () => counter.val++}, "👍"),
        button({class: 'btn btn-primary', onclick: () => counter.val--}, "👎")
    );
};

van.add(document.getElementById('wxFrame'), ReportFrame());