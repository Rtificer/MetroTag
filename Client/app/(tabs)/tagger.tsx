import React, { useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import Slider from '@react-native-community/slider';
import Arrow from '../../components/Arrow';
import { RouteProp, useRoute } from '@react-navigation/native';

type TaggerScreenRouteProp = RouteProp<{ params: { name: string } }, 'params'>;

const Tagger = () => {
	const [angle, setAngle] = useState(0);
	const route = useRoute<TaggerScreenRouteProp>();
	const name = route.params?.name || 'NoUserName';

	return (
		<View style={styles.container}>
			<Text style={styles.nameText}>Your name: {name}</Text>
			<Arrow angleOffset={angle} />
			<Slider
				style={styles.slider}
				minimumValue={0}
				maximumValue={360}
				value={angle}
				onValueChange={setAngle}
				step={1}
			/>
		</View>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
		backgroundColor: '#1e1e1e',
		padding: 20,
		color: '#fefefe'
	},
	nameText: {
		fontSize: 20,
		marginBottom: 20
	},
	slider: {
		transform: 'translate3d(0, -250px, 0)',
		width: 300,
		height: 40
	}
});

export default Tagger;
