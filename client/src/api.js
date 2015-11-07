import {game_state, types} from  './dummy.js';
import fetch_ from 'fetch';

async function fetch(url, options) {
	try {
		const response = await fetch_(url, {
			credentials: 'same-origin',
			...options
		});
		const json = await response.json();
		return json;
	} catch (err) {
		console.error(err.stack);
		throw err;
	}
}

async function get(url) {
	return await fetch(url, { method: 'get' });
}

async function post(url, body = {}) {
	const data = new FormData();

	for (let key in body) {
		data.append(key, body[key]);
	}

	return await fetch(url, {
		method: 'post',
		body: data
	});
}

export async function getGameState() {
	// return game_state;
	return await get('/game_state');
};

export async function getTypes() {
	return await get('/types');
};

export async function postBrewAction(recipeId) {
	return await post('/action_brew', { recipe_id: recipeId });
};

export async function postCollectAction(recipeId) {
	return await post('/action_collect');
};
