import React from 'react';
import ProgressIcon from './ProgressIcon';

import {find} from '../data';

export default class Stage extends React.Component {
	static contextTypes = {
		dispatch: React.PropTypes.func.isRequired,
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {actions} = this.props;
		const {types} = this.context;

		return <div className='queue'>
			{actions && actions.map((action) => {
				const recipe = find(types.recipes, action.recipe_id);
				return (
					<ProgressIcon duration={recipe.duration} end={action.tick}>
						<div style={{ background: 'red', width: 100, height: 100 }}></div>
					</ProgressIcon>
				);
			})}
		</div>;
	}
}
