import React from 'react';
import classnames from 'classnames';
import ProgressIcon from './ProgressIcon';

import {find} from '../data';
import * as unitTypes from '../resources/units';
import collectIcon from '../resources/collect.png';

class QueueItem extends React.Component {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {action} = this.props;

		let content;

		if (action.type === 'brew_action') {
			const recipe = find(this.context.types.recipes, action.recipe_id);
			const unitType = find(this.context.types.unit_types, recipe.unit_type_id);
			content = <img src={unitTypes[unitType.image].icon} />;
		} else if (action.type === 'collect_action') {
			content = <img src={collectIcon} />;
		}

		return (
			<div className={classnames('queue-item', action.type)}>
				{content}
			</div>
		);
	}
}

export default class Queue extends React.Component {
	static contextTypes = {
		dispatch: React.PropTypes.func.isRequired,
	}

	render() {
		const {actions} = this.props;
		const {types} = this.context;

		return <div className='queue'>
			{actions && actions.map((action) => {
				return (
					<ProgressIcon start={action.start} end={action.end} round key={action.id}>
						<QueueItem action={action} />
					</ProgressIcon>
				);
			})}
		</div>;
	}
}
