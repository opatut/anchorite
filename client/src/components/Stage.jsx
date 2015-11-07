import React from 'react';

import Item from './Item';
import HoverButton from './HoverButton';
import {find} from '../data';

export default class Stage extends React.Component {
	static contextTypes = {
		dispatch: React.PropTypes.func.isRequired,
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {items} = this.props;
		const {dispatch} = this.context;

		const onClick = item_type_id => event => {
			event.preventDefault();

			dispatch({
				type: 'stage.remove',
				item_type_id,
				count: 1,
			});
		}


		return <div className='stage'>
			<div className="items">
				{items && items.map(({item_type_id, count}, i) => {
					const itemType = find(this.context.types.item_types, item_type_id);
					return <HoverButton color='red' icon='&ndash;' onClick={onClick(item_type_id)} key={`${item_type_id}-${i}-${count}`}>
						<Item itemType={itemType} count={count} />
					</HoverButton>;
				})}
			</div>
			{items && items.toArray().length > 0 && (
				<div className="stage-button">
					<button onClick={() => dispatch({ type: 'stage.confirm' })}>Mix it!</button>
					<button onClick={() => dispatch({ type: 'stage.clear' })}>Nah, nevermind!</button>
				</div>
			)}
		</div>;
	}
}
