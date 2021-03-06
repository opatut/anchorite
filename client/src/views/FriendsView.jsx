import React from 'react';
import {BaseComponent} from '../BaseComponent';

export default class FriendsView extends BaseComponent {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
		dispatch: React.PropTypes.func.isRequired,
	}

	render() {
		const {dispatch, types} = this.context;

		const {friends} = types;

		async function addFriend(event) {
			event.preventDefault();

			const input = this.refs.username;

			const username = input.value;

			try {
				await dispatch({ type: 'friends.add', username });
				dispatch({ type: 'reload.full' });
				input.value = '';
			} catch (err) {
				alert(`User ${username} not found.`);
				console.error(err);
			}
		}

		return <div className="friends-view">
			There are no friends. Just enemies!

			<ul className="friends-list">
				{friends.map(friend => {
					function onClick() {
						// close friends panel
						dispatch({
							type: 'friends.toggle'
						});
						// open attack panel
						dispatch({
							type: 'attacks.toggle',
							targetUserId: friend.id
						});
					}

					return 	<li key={friend.id}>
						{friend.name}
						<button className="button red" onClick={onClick}>Attack!</button>
					</li>;
				})}
			</ul>

			<form className="friend-form">
				<input type="text" placeholder="Enter username" ref="username" />
				<button className="button green" onClick={this::addFriend}>Add neighbor</button>
			</form>
		</div>;
	}
}
