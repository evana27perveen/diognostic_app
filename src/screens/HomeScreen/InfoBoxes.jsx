import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useCookies } from 'react-cookie';

const InfoBoxes = () => {
  const [token] = useCookies(['myToken']);
  const [group] = useCookies(['myGroup']);
  const [appointmentsRunning, setAppointmentsRunning] = useState(0);
  const [appointmentsCompleted, setAppointmentsCompleted] = useState(0);
  const [totalTests, setTotalTests] = useState(0);
  const [profileStatus, setProfileStatus] = useCookies(['profileStatus']);


  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    console.log(token);
    try {
      const response = await fetch('http://192.168.0.106:8000/api/main/user-home-data/', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token.access_token}`,
        },
      });
      const data = await response.json();
      console.log(data);
  
      if (data !== null) {
        setAppointmentsRunning(data.appointment_running);
        setAppointmentsCompleted(data.appointment_completed);
        setTotalTests(data.total_tests);
        setProfileStatus("profile", data.profile);
      }
    } catch (error) {
      console.log('Error fetching data:', error);
    }
  };
  

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <View style={[styles.card, styles.topLeftCard]}>
          <Text style={styles.title}>Current Appointments</Text>
          <Text style={styles.value}>{appointmentsRunning}</Text>
        </View>
        <View style={[styles.card, styles.topRightCard]}>
          <Text style={styles.title}>Passed Appointments</Text>
          <Text style={styles.value}>{appointmentsCompleted}</Text>
        </View>
      </View>
      <View style={styles.row}>
        <View style={[styles.card, styles.bottomLeftCard]}>
          <Text style={styles.title}>Total Tests</Text>
          <Text style={styles.value}>{totalTests}</Text>
        </View>
        <View style={[styles.card, styles.bottomRightCard]}>
          <Text style={styles.title}>Total Feedbacks</Text>
          <Text style={styles.value}>187</Text>
        </View>
      </View>
    </View>
  );
};



const styles = StyleSheet.create({
  container: {
    flexDirection: 'column',
    marginTop: 0,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
    width: '100%',
  },
  card: {
    flex: 1,
    height: 100,
    margin: 5,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#3180e7',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  topLeftCard: {
    borderTopLeftRadius: 40,
    borderTopRightRadius: 0,
    borderBottomRightRadius: 30,
    borderBottomLeftRadius: 0,
    backgroundColor: 'lightblue',
  },
  topRightCard: {
    borderTopLeftRadius: 40,
    borderTopRightRadius: 0,
    borderBottomRightRadius: 30,
    borderBottomLeftRadius: 0,
    backgroundColor: 'lightblue',
  },
  bottomLeftCard: {
    borderTopLeftRadius: 40,
    borderTopRightRadius: 0,
    borderBottomRightRadius: 30,
    borderBottomLeftRadius: 0,
    backgroundColor: 'lightblue',
  },
  bottomRightCard: {
    borderTopLeftRadius: 40,
    borderTopRightRadius: 0,
    borderBottomRightRadius: 30,
    borderBottomLeftRadius: 0,
    backgroundColor: 'lightblue',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  value: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});

export default InfoBoxes;
