import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import {StocksView} from './components/StocksView'
import {StockDetailsView} from './components/StockDetailsView'

export const App = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <Redirect to="/stocks" />
                </Route>
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
