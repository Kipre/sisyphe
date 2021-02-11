// document.getElementById('get')

/* configurations */
const config = {
    historyLength: 10
}

const actions = {
    save: async()=>{
        const res = await fetch('save');
        console.log(await res.json());
    }
    ,
    ok: async()=>{
        if (!state.labels.size)
            return;
        fetch("label", {
            method: "POST",
            body: JSON.stringify({
                id: state.id,
                label: Array.from(state.labels).join(',')
            })
        }).then(res=>{
            if (res.ok)
                get();
        }
        );
    }
}

/* global state */
const view = {};
const state = {
    labels: new Set()
};

window.onload = async()=>{
    const response = await fetch('job');
    const job = await response.json();
    setJob(job);
    get();
}

document.addEventListener('keydown', e=>{
    if (e.key == 'Enter' || e.key == 'w') {
        e.preventDefault();
        actions.ok();
    }
}
);

async function get(id) {
    const response = await fetch('example' + (id ? '/' + id.toString() : ''));
    const example = await response.json();
    console.log(example);
    setExample(example);
}

function setJob(job) {
    document.body.innerText = '';

    const main = document.createElement('div');
    main.classList.add('main');
    const toolbar = document.createElement('div');
    toolbar.classList.add('toolbar');

    const header = document.createElement('div');
    header.classList.add('header');

    const title = document.createElement('div');
    title.classList.add('title');
    title.innerText = "sisyphe: " + job.title;
    header.appendChild(title);

    view.progress = document.createElement('div');
    view.progress.classList.add('progress');
    view.progress.innerText = '0%';

    header.appendChild(view.progress);
    main.appendChild(header);

    const controls = document.createElement('div');
    controls.classList.add('actions');
    toolbar.appendChild(controls);

    if (job.multilabel) {
        controls.appendChild(button('OK', actions.ok));
    }
    controls.appendChild(button('save', actions.save));

    view.content = document.createElement('div');
    view.content.classList.add('content');
    main.appendChild(view.content);

    view.categories = document.createElement('div');
    view.categories.classList.add('categories');
    for (const cat of job.categories) {
        const button = document.createElement('button');
        button.innerText = cat;
        button.onclick = ()=>{
            state.labels.has(cat) ? state.labels.delete(cat) : state.labels.add(cat);
            button.classList.toggle('selected');
            if (!job.multilabel) {
                actions.ok();
            }
        }
        ;
        view.categories.appendChild(button);
    }
    main.appendChild(view.categories);

    view.history = document.createElement('div');
    view.history.classList.add('history');
    toolbar.appendChild(view.history);

    document.body.appendChild(main);
    document.body.appendChild(toolbar);
}

function setExample(example) {
    if (state.example) {
        historyAdd(state);
    }
    state.labels.clear();
    for (let i = 0; i < view.categories.children.length; i++)
        view.categories.children[i].classList.remove('selected')
    state.id = example.id;
    state.example = example.example;
    view.progress.innerText = example.progress;
    view.content.innerHTML = example.example;
}

function historyAdd({id, example, labels}) {
    const children = view.history.children;
    for (let i = config.historyLength; i < children.length; i++) {
        children[i].remove();
    }
    const item = document.createElement('div');
    item.innerHTML = example.slice(0, 100);
    for (const label of labels) {
        item.appendChild(makeClass(label));
    }
    item.onclick = ()=>get(id);
    view.history.prepend(item);
}

function makeClass(label) {
    const element = document.createElement('span');
    element.classList.add('label');
    element.innerText = label;
    return element;
}

function button(name, callback) {
    const button = document.createElement('button');
    button.innerText = name;
    button.onclick = callback;
    return button;
}
