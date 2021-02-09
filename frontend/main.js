// document.getElementById('get')

/* global state */
const job = {};
const view = {};

window.onload = async ()=>{
    const response = await fetch('job');
    const obj = await response.json();
    job.title = obj.title;
    job.categories = obj.categories;
    job.id = -1;
    setJob(job, view);
    next();
}

async function next() {
    const response = await fetch('next');
    const example = await response.json();
    console.log(example);
    setExample(example, view);
}

function setJob(job, view) {
    document.body.innerText = '';
    
    view.header = document.createElement('div');
    view.header.classList.add('header');

    view.title = document.createElement('div');
    view.title.classList.add('title');
    view.title.innerText = "sisyphe: " + job.title;
    view.header.appendChild(view.title);
    
    view.progress = document.createElement('div');
    view.progress.classList.add('progress');
    view.progress.innerText = '0%';
    view.header.appendChild(view.progress);
    document.body.appendChild(view.header);
    
    
    view.actions = document.createElement('div');
    view.actions.classList.add('actions');
    document.body.appendChild(view.actions);

    for (const action of ['save', 'undo']) {
        const button = document.createElement('button');
        button.classList.add('action-button');
        button.innerText = action;
        button.onclick = async ()=>{
            const res = await fetch(`/${action}`);
            const obj = await res.json();
            if (obj.id)
                setExample(obj, view);
            else console.log(obj)
        }
        view.actions.appendChild(button);
    }

    view.content = document.createElement('div');
    view.content.classList.add('content');
    document.body.appendChild(view.content);
    
    view.buttons = document.createElement('div');
    view.buttons.classList.add('buttons');
    for (const cat of job.categories) {
        const button = document.createElement('button');
        button.classList.add('label-button');
        button.innerText = cat.name;
        button.onclick = ()=>{
            fetch("/label", {
              method: "POST", 
              body: JSON.stringify({id: job.id, label: cat.label})
            }).then(res => {
              if (res.ok) next();
            });
        }
        view.buttons.appendChild(button);
    }
    document.body.appendChild(view.buttons);
}

function setExample(example, view) {
    job.id = example.id;
    view.progress.innerText = example.progress;
    view.content.innerHTML = example.example;
}

function undo() {
    fetch("/undo", {
      method: "POST", 
      body: JSON.stringify({})
    }).then(res => {
      console.log("Request complete! response:", res);
    });
}