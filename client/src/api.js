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
	return await post('/action/brew', {
		recipe_id: recipeId
	});
};

export async function postCollectAction(recipeId) {
	return await post('/action/collect');
};

export async function postAttackAction(targetUserId, unitIds) {
	return await post('/action/attack', {
		target_user_id: targetUserId,
		unit_ids: unitIds.join(',')
	});
};

export async function postAddFriend(username) {
	return await post('/add_friend', {username});
};
