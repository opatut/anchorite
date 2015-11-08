import React from 'react';
import {BaseComponent} from '../BaseComponent';
import {Unit} from '../components';
import {find} from '../data';
import clock from '../clock';

function formatDuration(s_) {
	let s = Math.round(s_);
    let hours   = Math.floor(s / 3600);
    let minutes = Math.floor((s - (hours * 3600)) / 60);
    let seconds = s - (hours * 3600) - (minutes * 60);
    if (hours && minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}

	return (hours ? `${hours}h ` : '') + `${minutes}:${seconds}`;
}

@clock.listen
export default class AttacksView extends BaseComponent {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
		dispatch: React.PropTypes.func.isRequired,
	}

	render() {
		const {dispatch, types} = this.context;

		const {friends} = types;

		const {attackTargetUserId, units, tick} = this.props;

		const target = find(types.friends, attackTargetUserId);

		if (target) {
			async function send(event) {
				event.preventDefault();

				try {
					await dispatch({
						type: 'attack',
						targetUserId: attackTargetUserId,
						unitIds: units.map((u) => u.id),
					});
				} catch (err) {
					alert('Cannot attack right now');
					console.error(err);
				}

				await dispatch({
					type: 'reload'
				});

				await dispatch({
					type: 'attacks.toggle'
				});
			}

			return <div className="attacks-view">
				Attacking {target.name}
				<div onClick={send}>Send all units</div>
			</div>;
		} else {
			const {outgoing, incoming, currentUser} = this.props;

			const mapAttack = attack => {
				const outgoing = attack.target_user_id !== types.current_user.id;
				const users    = [...types.friends, types.current_user];
				const fromUser = find(users, attack.user_id);
				const toUser   = find(users, attack.target_user_id);

				const time = formatDuration(Math.max(0, attack.end - tick));

				return <li key={attack.id}>
					<div>{outgoing ? `Attacking ${toUser.name} in` : `From ${fromUser.name} in`} {time}</div>
					<div className='units'>
						{ attack.units && attack.units.map(unit => <Unit height={4} {...unit} key={unit.id} />) }
					</div>
				</li>;
			}

			const attacks = [...outgoing, ...incoming].sort((a, b) => a.end - b.end);

			return <div className="attacks-view">
				<ul>
					{attacks.map(mapAttack)}
				</ul>
				<div>{outgoing.length} out / {incoming.length} in</div>
			</div>;
		}
	}
}
