import React from 'react';

import Item from './components/Item';
import HoverButton from './components/HoverButton';

export default class App extends React.Component {
	render() {
		return <div>
			<HoverButton color='green' icon='+'>
				<Item itemType={{icon: 'pebble', name: 'Pebble'}} count={12} />
			</HoverButton>
		</div>;
	}
}
