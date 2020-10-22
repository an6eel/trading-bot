import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import {StocksView} from './components/StocksView'
import {StockDetailsView} from './components/StockDetailsView'

export const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/stocks">
                    <StocksView/>
                </Route>
                <Route path="/stockdetails">
                    <StockDetailsView/>
                </Route>
            </Switch>
        </Router>
    )
}


export default App;
