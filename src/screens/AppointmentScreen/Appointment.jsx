import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import Header from '../HomeScreen/Header';
import BottomNavBar from '../HomeScreen/BottomNavBar';
import AppointmentCarts from './AppointmentCarts';
import AppointmentForm from './AppointForm';

const { height } = Dimensions.get('window');
const formContainerHeight = height * 0.38;

const Appointment = ({ route }) => {
  const { cartList, cartItems } = route.params;

  return (
    <View style={styles.container}>
      <Header title="Appointments" />
      <View style={styles.contentContainer}>
        <View style={styles.cartContainer}>
          <Text style={styles.cartTitle}>Selected Cards:</Text>
          <AppointmentCarts cartItems={cartItems} />
        </View>
        <View style={[styles.formContainer, { height: formContainerHeight }]}>
          <AppointmentForm cartList={cartList} />
        </View>
      </View>
      <BottomNavBar cartList={cartList} cartItems={cartItems} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    margin: 5,
    flexDirection: 'column',
    width: '100%',
  },
  contentContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cartContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f9f9f9',
    marginBottom: 10,
  },
  cartTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  formContainer: {
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    marginBottom: 10,
  },
});

export default Appointment;
