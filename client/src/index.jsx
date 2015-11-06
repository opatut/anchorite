import '../styles/index.scss';

import React from 'react';
import {render} from 'react-dom';

import App from './App.jsx';

const container = document.getElementById('container');
render(<App />, container);
